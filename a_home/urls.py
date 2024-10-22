from django.urls import path, include
from a_home.views import *

urlpatterns = [
    path('', home_view, name='home'),

    # path('members/',test,name='members')
    
]