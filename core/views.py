from django.shortcuts import render
from accounts.decorators import role_required


def home(request):
    return render(request, 'core/home.html')

@role_required(['ADMIN'])
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')

@role_required(['TEAMLEAD'])
def department_dashboard(request):
    return render(request, 'core/department_dashboard.html')

@role_required(['EMPLOYEE'])
def employee_dashboard(request):
    return render(request, 'core/employee_dashboard.html')
