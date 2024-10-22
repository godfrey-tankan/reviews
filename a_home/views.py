from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from a_users.models import *
from .forms import *
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from a_bot.views import get_text_message_input,send_message
from django.contrib.auth.decorators import login_required
from .models import *


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
            demographic_data = form.save(commit=False)
            demographic_data.user_id = request.user
            demographic_data.save()
            return redirect('thank_you')
    else:
        form = DemographicDataForm()
    return render(request, 'demographic_data.html', {'form': form})


@login_required
def job_satisfaction_view(request):
    questions = JobSatisfactionQuestion.objects.all()

    if request.method == 'POST':
        form = JobSatisfactionForm(request.POST, questions=questions)
        if form.is_valid():
            for field_name, response in form.cleaned_data.items():
                question_id = int(field_name.split('_')[1])
                question = JobSatisfactionQuestion.objects.get(id=question_id)
                LikertScaleAnswer.objects.create(user_id=request.user,question=question, response=response)
            return redirect('thank_you') 
    else:
        form = JobSatisfactionForm(questions=questions)

    return render(request, 'job_satisfaction.html', {'form': form})