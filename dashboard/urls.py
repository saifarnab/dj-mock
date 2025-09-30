from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('services', views.service_list_view, name='service_list'),
    path('create-service', views.create_service_view, name='create_service'),
    path('create-endpoint', views.create_endpoint_view, name='create_endpoint'),
]
