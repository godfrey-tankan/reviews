from django.shortcuts import redirect, get_object_or_404
from .models import DemographicData
from a_users.models import User

def check_user_feedback(request):
    user_id = request.user
    user = get_object_or_404(User, id=user_id)
    demographic_ob = DemographicData.objects.filter(user_id=user)
    if demographic_ob.exists():
        return redirect('your_feedback')
    