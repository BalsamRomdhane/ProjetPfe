from django.urls import path
from . import views

urlpatterns = [
    path('generate/<int:doc_id>/', views.generate_audit_report, name='generate_audit_report'),
]
