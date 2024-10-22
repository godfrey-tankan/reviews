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
from django.db.models import Count, Sum, Avg




# Create your views here.
def home_view(request):
    return render(request,'home.html')

@login_required
def staff_dashboard_view(request):
    total_participants = LikertScaleAnswer.objects.values('user_id').distinct().count()
    
    most_proper_department = DemographicData.objects.values('department').annotate(
        avg_feedback=Avg('likertscaleanswer__response')
    ).order_by('-avg_feedback').first()

    average_qualification = DemographicData.objects.aggregate(
        Avg('highest_qualification')
    )

    context = {
        'total_participants': total_participants,
        'most_proper_department': most_proper_department,
        'average_qualification': average_qualification,
    }

    return render(request, 'staff/staff_dashboard.html', context)

@login_required
def aggregated_feedback_view(request):
    total_responses = LikertScaleAnswer.objects.count()

    question_summary = {}

    questions = JobSatisfactionQuestion.objects.all()

    for question in questions:
        responses = LikertScaleAnswer.objects.filter(question=question)
        count_responses = responses.count()
        
        if count_responses > 0:
            avg_response = responses.aggregate(Avg('response'))['response__avg']
            percentage_positive = responses.filter(response__gte=4).count() / count_responses * 100
            
            question_summary[question] = {
                'average': avg_response,
                'percentage_positive': percentage_positive,
                'count': count_responses
            }

    departments_feedback = DemographicData.objects.values('department').annotate(
        avg_feedback=Avg('likertscaleanswer__response')
    ).order_by('avg_feedback')

    worst_department = departments_feedback.first() if departments_feedback else None

    salary_complaints = LikertScaleAnswer.objects.filter(
        question__category='pay', 
        response__lte=3
    ).count()

    context = {
        'total_responses': total_responses,
        'question_summary': question_summary,
        'worst_department': worst_department,
        'salary_complaints': salary_complaints
    }

    return render(request, 'aggregated_feedback.html', context)

@login_required
def demographic_data_view(request):
    if request.method == 'POST':
        form = DemographicDataForm(request.POST)
        if form.is_valid():
            demographic_data = form.save(commit=False)
            demographic_data.user_id = request.user
            demographic_data.save()
            return redirect('job_satisfaction')
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

def thank_you(request):
    return render(request, 'thank_you.html')