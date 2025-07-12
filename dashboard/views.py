from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required(login_url='user_management:login')
def dashboard_view(request):
    return render(request, 'dashboard/dashboard.html')