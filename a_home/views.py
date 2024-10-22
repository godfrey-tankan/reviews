from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from a_users.models import *
from .forms import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from a_bot.views import get_text_message_input,send_message
from django.contrib.auth.decorators import login_required
from .models import SurveyAnswer


# Create your views here.
@login_required
def home_view(request):
    all_users = Individual.objects.all()
    all_groups =Group.objects.all()
    return render(request,'home.html',{'users': all_users,'groups': all_groups})

@login_required
def demographic_data_view(request):
    if request.method == 'POST':
        form = DemographicDataForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('thank_you')
    else:
        form = DemographicDataForm()
    return render(request, 'demographic_data.html', {'form': form})


@login_required
def survey_results_view(request):
    if request.user.is_staff:  # Assuming managing people have 'staff' status
        survey_answers = SurveyAnswer.objects.all()  # Fetch all answers
        return render(request, 'survey_results.html', {'survey_answers': survey_answers})
    return redirect('home')  
