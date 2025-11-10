"""
URL configuration for mockapi project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path(f"{settings.INTERNAL_BASE_PREFIX}/admin/", admin.site.urls),
    path(f"{settings.EXTERNAL_BASE_PREFIX}/account/", include('accounts.urls')),
    path(f"{settings.EXTERNAL_BASE_PREFIX}/dashboard/", include('dashboard.urls')),
    path(f"{settings.EXTERNAL_BASE_PREFIX}/", include('mocks.urls')),

]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

