from django.shortcuts import render
from accounts.decorators import role_required


def home(request):
    return render(request, 'core/home.html')

@role_required(['ADMIN'])
def admin_dashboard(request):
    return render(request, 'core/admin_dashboard.html')

@role_required(['ADMIN'])
def admin_users(request):
    # stubbed user/department list; views should populate with real data
    return render(request, 'core/admin_users.html', {
        'users': [],
        'departments': [],
    })

@role_required(['ADMIN'])
def departments_list(request):
    return render(request, 'core/departments_list.html')

@role_required(['ADMIN','TEAMLEAD'])
def reports(request):
    return render(request, 'core/reports.html')

@role_required(['TEAMLEAD'])
def department_dashboard(request):
    return render(request, 'core/department_dashboard.html')

@role_required(['TEAMLEAD'])
def analysis_list(request):
    return render(request, 'core/analysis_list.html')

@role_required(['EMPLOYEE'])
def employee_dashboard(request):
    return render(request, 'core/employee_dashboard.html')
