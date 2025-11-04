from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from helpers.utils import service_path
from mocks.models import MockEndpoint, MockService, BasicAuthConfig, ApiKeyAuthConfig, JWTAuthConfig, MockRule


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
        'host': service_path(request)

    }

    return render(request, 'dashboard/dashboard.html', context)


@login_required(login_url='login')
def service_list_view(request):
    services = MockService.objects.get_services_by_user(request.user)
    context = {
        'page_nav_title': 'Mock Services',
        'services': services,
        'host': service_path(request)
    }
    return render(request, 'dashboard/services.html', context)


@login_required(login_url='login')
def endpoint_list_view(request):
    endpoints = MockEndpoint.objects.get_endpoints(request.user)
    context = {
        'page_nav_title': 'Mock Endpoints',
        'endpoints': endpoints,
        'host': service_path(request)
    }
    return render(request, 'dashboard/endpoints.html', context)


@login_required(login_url='login')
def create_service_view(request):
    services = MockService.objects.get_services_by_user(request.user)

    if request.method == "POST":
        service_name = str(request.POST.get("serviceName")).strip()
        base_url = str(request.POST.get("baseUrl")).strip('/').strip()
        status_value = request.POST.get("status")
        status = True if status_value == "1" else False

        form_data = {
            'page_nav_title': 'Create Mock Service',
            "serviceName": service_name,
            "baseUrl": base_url,
            "status": status_value,
        }

        # check service name availability
        if MockService.objects.check_service_by_name(service_name):
            messages.error(request, "Service name already available")
            return render(request, 'dashboard/create_service.html', {"form_data": form_data})

        # check path availability
        if MockService.objects.check_service_url_existence(base_url):
            messages.error(request, "Base url already available")
            return render(request, 'dashboard/create_service.html', {"form_data": form_data})

        new_service = MockService.objects.create_new_service(request.user, service_name, base_url, status)

        context = {
            'page_nav_title': 'Mock Services',
            'services': services,
            'endpoints': [],
            'selected_service_id': new_service.id,

        }

        return render(request, 'dashboard/services.html', context)

    return render(request, 'dashboard/create_service.html', {'page_nav_title': 'Create Mock Service', })


@login_required(login_url='login')
def create_endpoint_view(request):
    services = MockService.objects.get_services_by_user(request.user)

    if request.method == "POST":
        service_id = str(request.POST.get("serviceID")).strip()
        endpoint_name = str(request.POST.get("endpointName")).strip()
        end_point = str(request.POST.get("endPoint")).lstrip('/').strip()
        http_method = request.POST.get("httpMethod").strip()
        auth_type = request.POST.get("authType").strip()
        default_http_status = request.POST.get("defaultHttpStatus").strip()
        default_response = request.POST.get("defaultResponse").strip()
        status_value = request.POST.get("status")
        status = True if status_value == "1" else False

        form_data = {
            'page_nav_title': 'Create Mock Endpoint',
            "services": services,
            "selected_service_id": service_id,
            "endPoint": end_point,
            "endpointName": endpoint_name,
            "httpMethod": http_method,
            "authType": auth_type,
            "defaultHttpStatus": default_http_status,
            "defaultResponse": default_response,
            "status": status_value,
        }

        # # check endpoint availability
        # if MockEndpoint.objects.check_endpoint_existence(service_id, end_point):
        #     messages.error(request, "Endpoint already available")
        #     return render(request, 'dashboard/create_endpoint.html', form_data)

        # check service availability
        service = MockService.objects.get_service(service_id)
        if not service:
            messages.error(request, "You are not authorized to create this endpoint.")
            return render(request, 'dashboard/create_endpoint.html', form_data)

        # create new endpoint
        new_endpoint = MockEndpoint.objects.create_new_endpoint(service, end_point, http_method, auth_type,
                                                                default_http_status, default_response, status,
                                                                endpoint_name)

        # get the endpoints
        endpoints = MockEndpoint.objects.get_service_endpoints(service.id)

        context = {
            'page_nav_title': 'Mock Endpoints',
            'services': services,
            'endpoints': endpoints,
            'selected_service_id': new_endpoint.service.id,
        }

        return render(request, 'dashboard/endpoints.html', context)

    context = {
        'page_nav_title': 'Create Mock Endpoint',
        'services': services
    }

    return render(request, 'dashboard/create_endpoint.html', context)


@login_required(login_url='login')
def edit_service_view(request, service_id):
    if request.method == "POST":
        base_url = str(request.POST.get("baseUrl")).strip('/').strip()
        status_value = request.POST.get("status")
        status = True if status_value == "1" else False
        MockService.objects.update_service(service_id, request.user, base_url, status)

        # get the endpoints & services
        endpoints = MockEndpoint.objects.get_service_endpoints(service_id)
        services = MockService.objects.get_services_by_user(request.user)

        context = {
            'page_nav_title': 'Mock Services',
            'services': services,
            'endpoints': endpoints,
            'selected_service_id': service_id,
        }

        return render(request, 'dashboard/services.html', context)

    service = MockService.objects.get_service(service_id)
    context = {
        'page_nav_title': 'Edit Mock Service',
        'service': service,
    }
    return render(request, 'dashboard/edit_service.html', context)


@login_required(login_url='login')
def edit_endpoint_view(request, endpoint_id):
    if request.method == "POST":

        endpoint = MockEndpoint.objects.get_endpoint(endpoint_id)
        endpoint_name = str(request.POST.get("endpointName")).strip()
        end_point = str(request.POST.get("endPoint")).lstrip('/').strip()
        http_method = request.POST.get("httpMethod").strip()
        auth_type = request.POST.get("authType").strip()
        default_http_status = request.POST.get("defaultHttpStatus").strip()
        default_response = request.POST.get("defaultResponse").strip()
        status_value = request.POST.get("status")
        status = True if status_value == "1" else False

        form_data = {
            'endpoint': endpoint,
            'page_nav_title': 'Edit Mock Endpoint',
            "endPoint": end_point,
            "endpointName": endpoint_name,
            "httpMethod": http_method,
            "authType": auth_type,
            "defaultHttpStatus": default_http_status,
            "defaultResponse": default_response,
            "status": status_value,
        }

        # check endpoint name availability
        if MockEndpoint.objects.check_endpoint_name(request.user, endpoint_name, endpoint.id):
            messages.error(request, "Endpoint name already available")
            return render(request, 'dashboard/edit_endpoint.html', form_data)

        # check endpoint url availability
        if MockEndpoint.objects.check_endpoint_existence(endpoint.service.id, end_point, endpoint.id):
            messages.error(request, "Endpoint url already available")
            return render(request, 'dashboard/edit_endpoint.html', form_data)

        MockEndpoint.objects.update_endpoint(endpoint.id, request.user, endpoint.service, end_point, http_method,
                                             auth_type, default_http_status, default_response, status, endpoint_name)

        endpoints = MockEndpoint.objects.get_endpoints(request.user)
        context = {
            'page_nav_title': 'Mock Endpoints',
            'endpoints': endpoints,
        }
        return render(request, 'dashboard/endpoints.html', context)

    endpoint = MockEndpoint.objects.get_endpoint(endpoint_id)
    context = {
        'page_nav_title': 'Edit Mock Endpoint',
        'endpoint': endpoint,
    }
    return render(request, 'dashboard/edit_endpoint.html', context)


@login_required(login_url='login')
def basic_auth_list_view(request):
    auths = BasicAuthConfig.objects.get_basic_auths(request.user)
    context = {'page_nav_title': 'Auth / Basic Auth', 'auths': auths}
    return render(request, 'auths/basic_auths.html', context)


@login_required(login_url='login')
def api_key_auth_list_view(request):
    auths = ApiKeyAuthConfig.objects.get_api_key_auths(request.user)
    context = {'page_nav_title': 'Auth / API KEY', 'auths': auths}
    return render(request, 'auths/api_key_auths.html', context)


@login_required(login_url='login')
def jwt_auth_list_view(request):
    auths = JWTAuthConfig.objects.get_jwt_auths(request.user)
    context = {'page_nav_title': 'Auth / JWT Token', 'auths': auths}
    return render(request, 'auths/jwt_auths.html', context)


@login_required(login_url='login')
def create_basic_auth_view(request):
    services = MockService.objects.get_services_by_user(request.user)

    if request.method == "POST":
        service_id = str(request.POST.get("serviceID")).strip()
        username = str(request.POST.get("userName")).strip()
        password = request.POST.get("password").strip()
        failed_status = int(request.POST.get("unAuthStatus").strip())
        failed_response = request.POST.get("unAuthRes").strip()

        form_data = {
            'page_nav_title': 'Auth / Create Basic Auth',
            "services": services,
            "selected_service_id": service_id,
            "username": username,
            "password": password,
            "unAuthStatus": str(failed_status),
            "unAuthRes": failed_response
        }

        # check service availability
        service = MockService.objects.get_service(service_id)
        if not service:
            messages.error(request, "Service not available")
            return render(request, 'auths/create_basic_auth.html', form_data)

        # check basic auth availability
        if BasicAuthConfig.objects.check_basic_auth(service):
            messages.error(request, "Basic auth already available for this service")
            return render(request, 'auths/create_basic_auth.html', form_data)

        # create new basic auth
        BasicAuthConfig.objects.create_new_basic_auth(service, username, password, True, failed_status, failed_response)

        # get basic auths
        auths = BasicAuthConfig.objects.get_basic_auths(request.user)
        context = {'page_nav_title': 'Auth / Basic Auths', 'auth': auths}
        return render(request, 'auths/basic_auths.html', context)

    context = {'page_nav_title': 'Auth / Create Basic Auth', 'services': services}
    return render(request, 'auths/create_basic_auth.html', context)


@login_required(login_url='login')
def create_api_key_auth_view(request):
    services = MockService.objects.get_services_by_user(request.user)

    if request.method == "POST":
        service_id = str(request.POST.get("serviceID")).strip()
        key_name = str(request.POST.get("keyName")).strip()
        key_value = request.POST.get("keyValue").strip()
        added_to = request.POST.get("addedTo").strip()
        failed_status = int(request.POST.get("unAuthStatus").strip())
        failed_response = request.POST.get("unAuthRes").strip()

        form_data = {
            'page_nav_title': 'Auth / Create API Key',
            "services": services,
            "selectedServiceId": service_id,
            "keyName": key_name,
            "keyValue": key_value,
            "addedTo": added_to,
            "unAuthStatus": str(failed_status),
            "unAuthRes": failed_response
        }

        # check service availability
        service = MockService.objects.get_service(service_id)
        if not service:
            messages.error(request, "Service not available")
            return render(request, 'auths/create_api_key_auth.html', form_data)

        # check api key auth availability
        if ApiKeyAuthConfig.objects.check_api_key_auth(service):
            messages.error(request, "API Key auth already available for this service")
            return render(request, 'auths/create_api_key_auth.html', form_data)

        # create new basic auth
        ApiKeyAuthConfig.objects.create_new_api_key_auth(service, key_name, key_value, added_to, True, failed_status,
                                                         failed_response)

        # get api key auths
        auths = ApiKeyAuthConfig.objects.get_api_key_auths(request.user)
        context = {'page_nav_title': 'Auth / API Keys', 'auths': auths}
        return render(request, 'auths/api_key_auths.html', context)

    context = {'page_nav_title': 'Auth / Create API Key', 'services': services}
    return render(request, 'auths/create_api_key_auth.html', context)


@login_required(login_url='login')
def create_jwt_auth_view(request):
    services = MockService.objects.get_services_by_user(request.user)

    if request.method == "POST":
        service_id = str(request.POST.get("serviceID")).strip()
        auth_header = str(request.POST.get("authHeader")).strip()
        token = request.POST.get("token").strip()
        failed_status = int(request.POST.get("unAuthStatus").strip())
        failed_response = request.POST.get("unAuthRes").strip()

        form_data = {
            'page_nav_title': 'Auth / Create JWT Token',
            "services": services,
            "selected_service_id": service_id,
            "authHeader": auth_header,
            "token": token,
            "unAuthStatus": str(failed_status),
            "unAuthRes": failed_response
        }

        # check service availability
        service = MockService.objects.get_service(service_id)
        if not service:
            messages.error(request, "Service not available")
            return render(request, 'auths/create_jwt_auth.html', form_data)

        # check JWT auth availability
        if JWTAuthConfig.objects.check_jwt_auth(service):
            messages.error(request, "JWT auth already available for this service")
            return render(request, 'auths/create_jwt_auth.html', form_data)

        # create new JWT auth
        JWTAuthConfig.objects.create_new_jwt_auth(service, auth_header, token, True, failed_status, failed_response)

        # get JWT auths
        auths = JWTAuthConfig.objects.get_jwt_auths(request.user)
        context = {'page_nav_title': 'Auth / JWT Tokens', 'auth': auths}
        return render(request, 'auths/jwt_auths.html', context)

    context = {'page_nav_title': 'Auth / Create JWT Token', 'services': services}
    return render(request, 'auths/create_jwt_auth.html', context)


@login_required(login_url='login')
def edit_basic_auth_view(request, basic_auth_id):
    if request.method == "POST":

        service_name = str(request.POST.get("serviceName")).strip()
        username = str(request.POST.get("userName")).strip()
        password = request.POST.get("password").strip()
        failed_status = int(request.POST.get("unAuthStatus").strip())
        failed_response = request.POST.get("unAuthRes").strip()

        form_data = {
            'page_nav_title': 'Auth / Edit Basic Auth',
            "serviceName": service_name,
            "username": username,
            "password": password,
            "unAuthStatus": str(failed_status),
            "unAuthRes": failed_response
        }

        basic_auth = BasicAuthConfig.objects.get_basic_auth(basic_auth_id)
        if not basic_auth:
            messages.error(request, "Invalid Request")
            return render(request, 'auths/edit_basic_auth.html', form_data)

        BasicAuthConfig.objects.update_basic_auth(basic_auth.id, request.user, username, password, True,
                                                  failed_status, failed_response)
        auths = BasicAuthConfig.objects.get_basic_auths(request.user)
        context = {'page_nav_title': 'Auth / Basic Auths', 'auths': auths}
        return render(request, 'auths/basic_auths.html', context)

    basic_auth = BasicAuthConfig.objects.get_basic_auth(basic_auth_id)
    context = {
        'page_nav_title': 'Auth / Edit Basic Auth',
        "authID": basic_auth.id,
        "serviceName": basic_auth.service.name,
        "username": basic_auth.username,
        "password": basic_auth.password,
        "unAuthStatus": basic_auth.failed_http_status,
        "unAuthRes": basic_auth.failed_response
    }
    return render(request, 'auths/edit_basic_auth.html', context)


@login_required(login_url='login')
def edit_api_key_auth_view(request, api_key_auth_id):
    if request.method == "POST":

        service_name = str(request.POST.get("serviceName")).strip()
        key_name = str(request.POST.get("keyName")).strip()
        key_value = str(request.POST.get("keyValue")).strip()
        added_to = request.POST.get("addedTo").strip()
        failed_status = int(request.POST.get("unAuthStatus").strip())
        failed_response = request.POST.get("unAuthRes").strip()

        form_data = {
            'page_nav_title': 'Auth / Edit API Key',
            "serviceName": service_name,
            "keyName": key_name,
            "keyValue": key_value,
            "addedTo": added_to,
            "unAuthStatus": str(failed_status),
            "unAuthRes": failed_response
        }

        api_key_auth = ApiKeyAuthConfig.objects.get_api_key_auth(api_key_auth_id)
        if not api_key_auth:
            messages.error(request, "Invalid Request")
            return render(request, 'auths/edit_api_key_auth.html', form_data)

        ApiKeyAuthConfig.objects.update_api_key_auth(api_key_auth.id, request.user, key_name, key_value, added_to,
                                                     True, failed_status, failed_response)
        auths = ApiKeyAuthConfig.objects.get_api_key_auths(request.user)
        context = {'page_nav_title': 'Auth / API Keys', 'auths': auths}
        return render(request, 'auths/api_key_auths.html', context)

    api_key_auth = ApiKeyAuthConfig.objects.get_api_key_auth(api_key_auth_id)
    context = {
        'page_nav_title': 'Auth / Edit API Key',
        "authID": api_key_auth.id,
        "serviceName": api_key_auth.service.name,
        "keyName": api_key_auth.key_name,
        "keyValue": api_key_auth.key_value,
        "addedTo": api_key_auth.add_to,
        "unAuthStatus": str(api_key_auth.failed_http_status),
        "unAuthRes": api_key_auth.failed_response
    }
    return render(request, 'auths/edit_api_key_auth.html', context)


@login_required(login_url='login')
def edit_jwt_auth_view(request, jwt_auth_id):
    if request.method == "POST":

        service_name = str(request.POST.get("serviceName")).strip()
        auth_header = str(request.POST.get("authHeader")).strip()
        token = request.POST.get("token").strip()
        failed_status = int(request.POST.get("unAuthStatus").strip())
        failed_response = request.POST.get("unAuthRes").strip()

        form_data = {
            'page_nav_title': 'Auth / Edit JWT Token',
            "serviceName": service_name,
            "authHeader": auth_header,
            "token": token,
            "unAuthStatus": str(failed_status),
            "unAuthRes": failed_response
        }

        jwt_auth = JWTAuthConfig.objects.get_jwt_auth(jwt_auth_id)
        if not jwt_auth:
            messages.error(request, "Invalid Request")
            return render(request, 'auths/edit_jwt_auth.html', form_data)

        JWTAuthConfig.objects.update_jwt_auth(jwt_auth.id, request.user, auth_header, token, True, failed_status,
                                              failed_response)
        auths = JWTAuthConfig.objects.get_jwt_auths(request.user)
        context = {'page_nav_title': 'Auth / JWT Tokens', 'auths': auths}
        return render(request, 'auths/jwt_auths.html', context)

    jwt_auth = JWTAuthConfig.objects.get_jwt_auth(jwt_auth_id)
    context = {
        'page_nav_title': 'Auth / Edit JWT Token',
        "authID": jwt_auth.id,
        "serviceName": jwt_auth.service.name,
        "authHeader": jwt_auth.auth_header,
        "token": jwt_auth.token,
        "unAuthStatus": str(jwt_auth.failed_http_status),
        "unAuthRes": jwt_auth.failed_response
    }
    return render(request, 'auths/edit_jwt_auth.html', context)


@login_required(login_url='login')
def rule_list_view(request):
    rules = MockRule.objects.get_rules(request.user)
    context = {'page_nav_title': 'Mock Rules', 'rules': rules}
    return render(request, 'rules/rules.html', context)


@login_required(login_url='login')
def create_rule_view(request):
    services = MockService.objects.get_services_by_user(request.user)
    selected_service_id = request.GET.get('serviceID')  # read selected service
    endpoints = MockEndpoint.objects.filter(service_id=selected_service_id) if selected_service_id else []

    if request.method == "POST":
        endpoint_id = str(request.POST.get("endpointID")).strip()
        source = str(request.POST.get("requestSource")).strip()
        data_format = str(request.POST.get("dataFormat")).strip()
        key = str(request.POST.get("key")).strip()
        key_value = str(request.POST.get("keyValue")).strip()
        resp_http_code = str(request.POST.get("respHttpCode")).strip()
        resp_body = str(request.POST.get("responseBody")).strip()
        status_value = request.POST.get("status")
        status = True if status_value == "1" else False

        endpoint = MockEndpoint.objects.get_endpoint(endpoint_id)
        MockRule.objects.create_rule(endpoint, source, data_format, key, key_value, resp_http_code, resp_body, status)

        rules = MockRule.objects.get_rules(request.user)
        context = {'page_nav_title': 'Create Rule', 'rules': rules}
        return render(request, 'rules/rules.html', context)

    context = {
        'page_nav_title': 'Create Rule',
        'services': services,
        'endpoints': endpoints,
        'selected_service_id': selected_service_id,
    }

    return render(request, 'rules/create_rule.html', context)


@login_required(login_url='login')
def edit_rule_view(request, rule_id):
    rule = MockRule.objects.get_rule(rule_id)

    if request.method == "POST":
        source = str(request.POST.get("requestSource")).strip()
        data_format = str(request.POST.get("dataFormat")).strip()
        key = str(request.POST.get("key")).strip()
        key_value = str(request.POST.get("keyValue")).strip()
        resp_http_code = str(request.POST.get("respHttpCode")).strip()
        resp_body = str(request.POST.get("responseBody")).strip()
        status_value = request.POST.get("status")
        status = True if status_value == "1" else False

        MockRule.objects.update_rule(rule_id, source, data_format, key, key_value, resp_http_code, resp_body, status)
        rules = MockRule.objects.get_rules(request.user)
        context = {'page_nav_title': 'Rules', 'rules': rules}
        return render(request, 'rules/rules.html', context)

    context = {
        'page_nav_title': 'Edit Rule',
        'ruleID': rule_id,
        'serviceName': rule.endpoint.service.name,
        'serviceUrl': rule.endpoint.service.base_path,
        'endpointName': rule.endpoint.endpoint_name,
        'endpointUrl': rule.endpoint.path,
        'requestSource': rule.request_source,
        'dataFormat': rule.data_format,
        'key': rule.condition_field,
        'keyValue': rule.condition_value,
        'respHttpCode': rule.response_code,
        'responseBody': rule.response_body,
        'status': "1" if rule.is_active else "0",
    }

    return render(request, 'rules/edit_rule.html', context)


@login_required(login_url='login')
def details_service_view(request, service_id):
    service = MockService.objects.get_service(service_id)
    context = {
        'page_nav_title': 'Mock Service Details',
        'service': service,
        'host': service_path(request)
    }
    return render(request, 'dashboard/service_details.html', context)


@login_required(login_url='login')
def details_endpoint_view(request, endpoint_id):
    endpoint = MockEndpoint.objects.get_endpoint(endpoint_id)
    context = {
        'page_nav_title': 'Mock Endpoint Details',
        'endpoint': endpoint,
        'host': service_path(request)
    }
    return render(request, 'dashboard/endpoint_details.html', context)


@login_required(login_url='login')
def details_basic_auth_view(request, basic_auth_id):
    ba = BasicAuthConfig.objects.get_basic_auth(basic_auth_id)
    context = {
        'page_nav_title': 'Basic Auth Details',
        'auth': ba,
    }
    return render(request, 'auths/basic_auth_details.html', context)


@login_required(login_url='login')
def details_api_key_auth_view(request, api_key_auth_id):
    ak = ApiKeyAuthConfig.objects.get_api_key_auth(api_key_auth_id)
    context = {
        'page_nav_title': 'Basic Auth Details',
        'auth': ak,
    }
    return render(request, 'auths/api_key_auth_details.html', context)


@login_required(login_url='login')
def details_jwt_auth_view(request, jwt_auth_id):
    jwt = JWTAuthConfig.objects.get_jwt_auth(jwt_auth_id)
    context = {
        'page_nav_title': 'JWT Auth Details',
        'auth': jwt,
    }
    return render(request, 'auths/jwt_auth_details.html', context)


@login_required(login_url='login')
def details_rule_view(request, rule_id):
    rule = MockRule.objects.get_rule(rule_id)
    context = {
        'page_nav_title': 'Rule Details',
        'rule': rule,
    }
    return render(request, 'rules/rule_details.html', context)
