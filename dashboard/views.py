from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from mocks.models import MockEndpoint, MockService


def dashboard_view(request):
    total_service = MockService.objects.get_total_service_count()
    total_endpoints = MockEndpoint.objects.get_total_endpoints_count()
    total_hits = MockEndpoint.objects.get_total_endpoints_hit_count()
    endpoints = MockEndpoint.objects.get_most_hit_endpoints()
    context = {
        'total_service': total_service,
        'total_endpoints': total_endpoints,
        'total_hits': total_hits,
        'endpoints': endpoints,
    }

    return render(request, 'dashboard/dashboard.html', context)


def service_list_view(request):
    user = User.objects.get(username='sma')
    services = MockService.objects.get_services_by_user(user)
    selected_service_id = None

    if request.method == "POST":
        selected_service_id = request.POST.get("service_id")
        endpoints = MockEndpoint.objects.get_service_endpoints(selected_service_id)
    else:
        endpoints = MockEndpoint.objects.get_most_hit_endpoints()

    context = {
        'services': services,
        'endpoints': endpoints,
        'selected_service_id': selected_service_id,

    }
    return render(request, 'dashboard/services.html', context)


def create_service_view(request):
    user = User.objects.get(username='sma')
    services = MockService.objects.get_services_by_user(user)
    selected_service_id = None

    if request.method == "POST":
        selected_service_id = request.POST.get("service_id")
        endpoints = MockEndpoint.objects.get_service_endpoints(selected_service_id)
    else:
        endpoints = MockEndpoint.objects.get_most_hit_endpoints()

    context = {
        'services': services,
        'endpoints': endpoints,
        'selected_service_id': selected_service_id,

    }
    return render(request, 'dashboard/create_service.html', context)
