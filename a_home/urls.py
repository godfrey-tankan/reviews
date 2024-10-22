from django.urls import path, include
from a_home.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('start/', demographic_data_view, name='start'),
    path('thank-you/', thank_you, name='thank_you'),
    path('job-satisfaction/', job_satisfaction_view, name='job_satisfaction'),
    path('aggregated-feedback/', aggregated_feedback_view, name='aggregated_feedback'),
    # path('members/',test,name='members')
    
]