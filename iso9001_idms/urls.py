from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('documents/', include('documents.urls')),
    path('analysis/', include('analysis.urls')),
    path('audits/', include('audits.urls')),
    path('', include('core.urls')),
]
