from django.urls import path, include
from a_home.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('start/', demographic_data_view, name='start'),
    # path('members/',test,name='members')
    
]