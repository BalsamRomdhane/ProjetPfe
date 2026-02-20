from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('department-dashboard/', views.department_dashboard, name='department_dashboard'),
    path('employee-dashboard/', views.employee_dashboard, name='employee_dashboard'),
]
