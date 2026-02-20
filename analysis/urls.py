from django.urls import path
from . import views

urlpatterns = [
    path('launch/<int:doc_id>/', views.launch_analysis, name='launch_analysis'),
    path('view/<int:doc_id>/', views.view_analysis, name='view_analysis'),
]
