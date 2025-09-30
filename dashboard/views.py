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

    if request.method == "POST":
        service_name = str(request.POST.get("serviceName")).strip()
        base_url = str(request.POST.get("baseUrl")).strip()
        status = True if request.POST.get("status") == "1" else False

        if MockService.objects.check_service_by_name(service_name):
            messages.error(request, "Service name already available")
            return render(request, 'dashboard/create_service.html', {})

        if MockService.objects.check_service_by_url(base_url):
            return render(request, 'dashboard/create_service.html', {})

        new_service = MockService.objects.create_new_service(user, service_name, base_url, status)
        endpoints = MockEndpoint.objects.get_service_endpoints(new_service.id)

        context = {
            'services': services,
            'endpoints': endpoints,
            'selected_service_id': new_service.id,

        }

        return render(request, 'dashboard/services.html', context)

    return render(request, 'dashboard/create_service.html', {})


def create_endpoint_view(request):
    user = User.objects.get(username='sma')
    services = MockService.objects.get_services_by_user(user)

    if request.method == "POST":
        pass

    context = {
        'services': services
    }

    return render(request, 'dashboard/create_endpoint.html', context)
