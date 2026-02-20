from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('callback/', views.oidc_callback, name='oidc_callback'),
    path('unauthorized/', views.unauthorized_view, name='unauthorized'),
    path('post-login/', views.post_login_redirect, name='post_login'),
]
