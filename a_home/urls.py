from django.urls import path, include
from a_home.views import *

urlpatterns = [
    path('', home_view, name='home'),
    path('individuals/',all_individuals_view, name='individual_list'),
    path('individuals/new/', individual_create_view, name='individual_create'),
    path('individuals/<int:pk>/edit/', individual_edit_view, name='individual_edit'),
    path('individuals/<int:pk>/delete/', individual_delete_view, name='individual_delete'),
    path('groups/', group_list_view, name='group_list'),
    path('groups/create/', group_create_view, name='group_create'),
    path('groups/<int:group_id>/', group_detail, name='group_detail'),
    path('groups/edit/<int:group_id>/', group_edit_view, name='group_edit'),
    path('group-action', manage_group_actions, name='perform_group_action'),
    path('groups/delete/<int:group_id>/', group_delete_view, name='group_delete'),
    path('groups/<int:group_id>/add-individuals/', add_individual_to_group, name='add_individual_to_group'),
    # path('members/',test,name='members')
    
]