from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_document, name='upload_document'),
    path('list/', views.list_documents, name='list_documents'),
]
