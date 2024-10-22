from django.shortcuts import render
import logging
from datetime import datetime
import json
import time
import random
from django.conf import settings
import requests as requests
import contextlib
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .responses import *
from django.db.models import OuterRef, Subquery
from django.core.files.base import ContentFile
from django.utils import timezone
import re

def get_greeting():
    current_hour = datetime.now().hour
    if 0 <= current_hour < 10:
        return "morning"
    elif 10 <= current_hour < 16:
        return "afternoon"
    else:
        return "evening"

def generate_response(response, wa_id, name,message_type=None,message_id=None):
    return f"Hi good {get_greeting()} {name}!"    

def get_text_message_input(recipient, text,name=None,template=False):

    if template:
        return json.dumps(
            {
                "messaging_product": "whatsapp",
                "recipient_type": "individual",
                "to": recipient,
                "type": "template",
                "template": {
                    "name": f"{name}",
                    "language": {"code": "en"},
                },
            }
        )
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {"preview_url": False, "body": text},
        }
    )

def send_message(data,template=False):
    headers = {
        "Content-type": "application/json",
        "Authorization": f"Bearer {settings.ACCESS_TOKEN}",
    }
    url = f"https://graph.facebook.com/{settings.VERSION}/{settings.PHONE_NUMBER_ID}/messages"
    try:
        response = requests.post(
            url, data=data, headers=headers, timeout=30
        )  
        response.raise_for_status()  # Raises an HTTPError if the HTTP request returned an unsuccessful status code
    except requests.Timeout:
        pass
        # logging.error("Timeout occurred while sending message")
        # return jsonify({"status": "error", "message": "Request timed out"}), 408
    except (    
        requests.RequestException
    ) as e:  # This will catch any general request exception
        pass
        # logging.error(f"Request failed due to: {e}")
        # return jsonify({"status": "error", "message": "Failed to send message"}), 500
    else:
        # Process the response as normal
        return response

def process_whatsapp_message(body):
    data = body
    try:
        phone_number_id = [contact['wa_id'] for contact in data['entry'][0]['changes'][0]['value']['contacts']]
    except Exception as e:
        phone_number_id = ""

    try:
        profile_name = data['entry'][0]['changes'][0]['value']['contacts'][0]['profile']['name']
    except Exception as e:
        profile_name = "User"

    try:
        process_message_file_type(
            body, phone_number_id, profile_name
        )
    except Exception as e:
        print(f"Error processing message: {e}")
        ...


def get_audio_message_input(phone_number_id, audio_id):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": phone_number_id,
            "type": "audio",
            "audio": {
                'id':audio_id
            },
        }
    )

def process_message_file_type(body, phone_number_id, profile_name):
    message = body["entry"][0]["changes"][0]["value"]["messages"][0]
    message_type = message["type"]
    message_id = None
    message_body = message["text"]["body"]
        
    if message_type == "audio":
        message_id = message["audio"]["id"]
        data = get_audio_message_input('263779586059', message_id)
        return send_message(data)
    elif message_type =='button':
        message_body = message["button"]["text"]
    
    elif message_type == "video":
        message_id = message["video"]["id"]
        data = get_video_message('263779586059', message_id)
        return send_message(data)
    
    elif message_type == "document":
        message_id = message["document"]["id"]
        
        data = get_document_message('263779586059', message_id)
        return send_message(data)

    elif message_type == "image":
        message_id = message["image"]["id"]
      
        return send_message(data)
    elif message_type == "text":
        message_body = message["text"]["body"]
        
    response = generate_response(message_body, phone_number_id, profile_name,message_type,message_id)
    data = get_text_message_input(phone_number_id, response, None, False)
    return send_message(data)


def send_message_template(recepient):
    return json.dumps(
    {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": f"{recepient}",
        "type": "template",
        "template": {
            "namespace": "7a757027_47cc_4bb8_997e_e1fdb0600675",
            "name": "clava_home2",
            "language": {
                "code": "en",
            }
        }
    }
)

def is_valid_whatsapp_message(body):
    
    """
    Check if the incoming webhook event has a valid WhatsApp message structure.
    """
    return (
        body.get("object")
        and body.get("entry")
        and body["entry"][0].get("changes")
        and body["entry"][0]["changes"][0].get("value")
        and body["entry"][0]["changes"][0]["value"].get("messages")
        and body["entry"][0]["changes"][0]["value"]["messages"][0]
    )


def broadcast_messages(name,ticket=None,message=None,phone_number=None,message_type=None,message_id=None):
    support_members = None
    for support_member in support_members:
        user_mobile = support_member.phone_number
        if user_mobile == phone_number:
            ...
        else:
            if message_type == "document":
                data = get_document_message(user_mobile, message_id)
                return send_message(data)
            if message_type == "image":
                data = get_image_message(user_mobile, message_id)
                return send_message(data)
            if message_type == "audio":
                data = get_audio_message_input(user_mobile, message_id)
                return send_message(data)
            
            
    return 'response'
  
def get_image_message(recipient, image_id):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "image",
            "image": {
                'id':f'{image_id}'
            },
        }
    )

def forward_message(message,number):
    data =get_text_message_input(number, message, None)
    return send_message(data)
    
def get_document_message(recipient, document_id, caption='New document'):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "document",
            "document": {
                "id": document_id,
                "filename": f"{caption}",
            },
        }
    )

def get_video_message(recipient, video_id):
    return json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "video",
            "video": {
                "id": video_id,
            },
        }
    )