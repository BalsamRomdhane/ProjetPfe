from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-dashboard/users/', views.admin_users, name='admin_users'),
    path('departments/', views.departments_list, name='departments_list'),
    path('reports/', views.reports, name='reports'),
    path('analysis/', views.analysis_list, name='analysis_list'),
    path('department-dashboard/', views.department_dashboard, name='department_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
]
