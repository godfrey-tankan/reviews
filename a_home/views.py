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
def survey_results_view(request):
    if request.user.is_staff:  # Assuming managing people have 'staff' status
        survey_answers = SurveyAnswer.objects.all()  # Fetch all answers
        return render(request, 'survey_results.html', {'survey_answers': survey_answers})
    return redirect('home')  


# Create new individual
@login_required
def individual_create_view(request):
    if request.method == 'POST':
        form = IndividualForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Individual added successfully!')
            return redirect('individual_list') 
    else:
        form = IndividualForm()
    return render(request, 'individuals/individual_create.html', {'form': form})

# Edit existing individual
@login_required
def individual_edit_view(request, pk):
    individual = get_object_or_404(Individual, pk=pk)
    if request.method == 'POST':
        form = IndividualForm(request.POST, instance=individual)
        if form.is_valid():
            form.save()
            messages.success(request, 'Individual updated successfully!')
            return redirect('individual_list')
    else:
        form = IndividualForm(instance=individual)
    return render(request, 'individuals/individual_edit.html', {'form': form, 'individual': individual})

# Delete an individual
@login_required
def individual_delete_view(request, pk):
    individual = get_object_or_404(Individual, pk=pk)
    if request.method == 'POST':
        individual.delete()
        messages.success(request, 'Individual deleted successfully!')
        return redirect('individual_list')
    return render(request, 'individuals/individual_delete.html', {'individual': individual})

@login_required
def all_individuals_view(request):
    individuals = Individual.objects.all()
    return render(request, 'individuals/individual_list.html', {'individuals': individuals})


# Create a new group
@login_required
def group_create_view(request):
    if request.method == "POST":
        form = GroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            return redirect('group_list')
    else:
        form = GroupForm()
    return render(request, 'groups/group_form.html', {'form': form})

# Edit an existing group
@login_required
def group_edit_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == "POST":
        form = GroupForm(request.POST, instance=group)
        if form.is_valid():
            form.save()
            return redirect('group_list')
    else:
        form = GroupForm(instance=group)
    return render(request, 'groups/group_form.html', {'form': form})

# Delete a group
@login_required
def group_delete_view(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if request.method == "POST":
        group.delete()
        return redirect('group_list') 
    return render(request, 'groups/group_confirm_delete.html', {'group': group})

# List all groups
@login_required
def group_list_view(request):
    groups = Group.objects.all()
    return render(request, 'groups/group_list.html', {'groups': groups})

# Add individuals to a group
@login_required
def add_individual_to_group(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    users = Individual.objects.all()

    if request.method == "POST":
        selected_users = request.POST.getlist('selected_users')
        current_members = group.members.values_list('id', flat=True)

        for user_id in selected_users:
            individual = get_object_or_404(Individual, id=user_id)
            group.members.add(individual)  

        for member_id in current_members:
            if str(member_id) not in selected_users:
                individual = get_object_or_404(Individual, id=member_id)
                group.members.remove(individual) 

        return redirect('group_detail', group_id=group.id)  

    return render(request, 'groups/add_individual_to_group.html', {'group': group, 'users': users})

@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    return render(request, 'groups/group_detail.html', {'group': group})

@login_required
def manage_group_actions(request):
    groups = Group.objects.all() 
    if request.method == "POST":
        group_id = request.POST.get('group')
        action = request.POST.get('action')
        message = request.POST.get('message', '')
        if action == 'send_message':
            relevent_group = get_object_or_404(Group, id=group_id)
            for member in relevent_group.members.all():
                data = get_text_message_input(member.phone, message,None)
                send_message(data)
        return redirect('home')

    return render(request, 'groups/add_individual_to_group.html', {'groups': groups})
def get_group_people_info(group_id):
    group = get_object_or_404(Group, id=group_id)
    return  [
        {
            "id": member.id,
            "firstname": member.firstname,
            "surname": member.surname,
            "email": member.email, 
            "phone_number": member.phone 
        } for member in group.members.all()
    ]
    

# @csrf_exempt
# def test(request):
#     x = get_group_people_info(1)
#     return JsonResponse(x, safe=False)



