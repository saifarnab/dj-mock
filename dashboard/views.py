from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from mocks.models import MockEndpoint, MockService


@login_required(login_url='login')
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


@login_required(login_url='login')
def service_list_view(request):
    services = MockService.objects.get_services_by_user(request.user)
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


@login_required(login_url='login')
def create_service_view(request):
    services = MockService.objects.get_services_by_user(request.user)

    if request.method == "POST":
        service_name = str(request.POST.get("serviceName")).strip()
        base_url = str(request.POST.get("baseUrl")).strip()
        status_value = request.POST.get("status")
        status = True if status_value == "1" else False

        form_data = {
            "serviceName": service_name,
            "baseUrl": base_url,
            "status": status_value,
        }

        if MockService.objects.check_service_by_name(service_name):
            messages.error(request, "Service name already available")
            return render(request, 'dashboard/create_service.html', {"form_data": form_data})

        if MockService.objects.check_service_url_existence(base_url):
            messages.error(request, "Base url already available")
            return render(request, 'dashboard/create_service.html', {"form_data": form_data})

        new_service = MockService.objects.create_new_service(request.user, service_name, base_url, status)

        context = {
            'services': services,
            'endpoints': [],
            'selected_service_id': new_service.id,

        }

        return render(request, 'dashboard/services.html', context)

    return render(request, 'dashboard/create_service.html', {})


@login_required(login_url='login')
def create_endpoint_view(request):
    services = MockService.objects.get_services_by_user(request.user)

    if request.method == "POST":
        service_id = str(request.POST.get("serviceID")).strip()
        end_point = str(request.POST.get("endPoint")).strip()
        http_method = request.POST.get("httpMethod").strip()
        auth_type = request.POST.get("authType").strip()
        default_http_status = request.POST.get("defaultHttpStatus").strip()
        default_response = request.POST.get("defaultResponse").strip()
        status_value = request.POST.get("status")
        status = True if status_value == "1" else False

        form_data = {
            "services": services,
            "selected_service_id": service_id,
            "end_point": end_point,
            "http_method": http_method,
            "auth_type": auth_type,
            "default_http_status": default_http_status,
            "default_response": default_response,
            "status": status_value,
        }

        # check endpoint availability
        if MockEndpoint.objects.check_endpoint_existence(service_id, end_point):
            messages.error(request, "Endpoint already available")
            return render(request, 'dashboard/create_endpoint.html', {"form_data": form_data})

        # check service availability
        service = MockService.objects.get_service(service_id, request.user)
        if not service:
            messages.error(request, "You are not authorized to create this endpoint.")
            return render(request, 'dashboard/create_endpoint.html', {"form_data": form_data})

        # create new endpoint
        new_endpoint = MockEndpoint.objects.create_new_endpoint(service, end_point, http_method, auth_type,
                                                                default_http_status, default_response, status)

        # get the endpoints
        endpoints = MockEndpoint.objects.get_service_endpoints(service.id)

        context = {
            'services': services,
            'endpoints': endpoints,
            'selected_service_id': new_endpoint.service.id,
        }

        return render(request, 'dashboard/services.html', context)

    context = {
        'services': services
    }

    return render(request, 'dashboard/create_endpoint.html', context)
