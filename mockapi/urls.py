"""
URL configuration for mockapi project.
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path
from django.urls.conf import include

urlpatterns = [
    path("mock-api/i/admin/", admin.site.urls),
    path("mock-api/e/", include('mocks.urls')),

]
