from django.db import models
from django.db.models import Sum


class MockEndpointManager(models.Manager):
    def get_most_hit_endpoints(self):
        return self.select_related('service').order_by('-hit_count')[:10]

    def get_service_endpoints(self, service_id):
        return self.select_related('service').filter(service__id=service_id)

    def get_endpoints(self, user):
        return self.filter(service__user=user).order_by('-created_at')

    def check_endpoint_name(self, user, endpoint_name):
        return self.filter(service__user=user, endpoint_name=endpoint_name).exists()

    def get_endpoint(self, endpoint_id, user):
        return self.filter(id=endpoint_id, service__user=user).last()

    def get_total_endpoints_count(self):
        return self.all().count()

    def get_total_endpoints_hit_count(self):
        return self.all().aggregate(total=Sum('hit_count'))['total']

    def check_endpoint_existence(self, user, service_id, url):
        return self.filter(service_user=user, service__id=service_id, path=url).exists()

    def create_new_endpoint(self, service, end_point, http_method, auth_type, default_http_status, default_response,
                            status, endpoint_name):
        return self.create(service=service, path=end_point, method=http_method, default_http_status=default_http_status,
                           default_response=default_response, auth_type=auth_type, is_active=status,
                           endpoint_name=endpoint_name)


class MockServiceManager(models.Manager):
    def get_total_service_count(self):
        return self.all().count()

    def get_services_by_user(self, user):
        return self.filter(user=user).order_by('-created_at')

    def create_new_service(self, user, name, url, is_active):
        return self.create(user=user, name=name, base_path=url, is_active=is_active)

    def check_service_by_name(self, name):
        return self.filter(name=name).exists()

    def check_service_url_existence(self, url):
        return self.filter(base_path=url).exists()

    def get_service(self, service_id, user):
        return self.filter(user=user, id=service_id).last()

    def get_service_without_user(self, service_id):
        return self.filter(id=service_id).last()

    def update_service(self, service_id, user, base_path, status):
        return self.filter(user=user, id=service_id).update(base_path=base_path, is_active=status)


class BasicAuthConfigManager(models.Manager):
    def get_basic_auths(self, user):
        return self.filter().order_by('-created_at')

    def get_basic_auth(self, user, basic_id):
        return self.filter(id=basic_id, service__user=user).last()

    def create_new_basic_auth(self, service, username, password, is_active):
        return self.create(service=service, username=username, password=password, is_active=is_active)

    def check_basic_auth(self, service):
        return self.filter(service=service).exists()

    def update_basic_auth(self, auth_id, user, username, password, status):
        return self.filter(service__user=user, id=auth_id).update(username=username, password=password,
                                                                  is_active=status)


class APIKeyAuthConfigManager(models.Manager):
    def get_api_key_auths(self, user):
        return self.filter().order_by('-created_at')

    def get_api_key_auth(self, user, api_key_id):
        return self.filter(id=api_key_id, service__user=user).last()

    def check_api_key_auth(self, service):
        return self.filter(service=service).exists()

    def create_new_api_key_auth(self, service, key_name, key_value, added_to, is_active):
        return self.create(service=service, key_name=key_name, key_value=key_value, add_to=added_to,
                           is_active=is_active)

    def update_api_key_auth(self, auth_id, user, key_name, key_value, added_to, status):
        return self.filter(service__user=user, id=auth_id).update(key_name=key_name, key_value=key_value,
                                                                  add_to=added_to, is_active=status)


class JWTAuthConfigManager(models.Manager):
    def get_jwt_auths(self, user):
        return self.filter().order_by('-created_at')

    def get_jwt_auth(self, user, jwt_id):
        return self.filter(id=jwt_id, service__user=user).last()

    def check_jwt_auth(self, service):
        return self.filter(service=service).exists()

    def create_new_jwt_auth(self, service, auth_header, token, is_active):
        return self.create(service=service, auth_header=auth_header, token=token, is_active=is_active)

    def update_jwt_auth(self, auth_id, user, auth_header, token, status):
        return self.filter(service__user=user, id=auth_id).update(auth_header=auth_header, token=token,
                                                                  is_active=status)


class MockRuleManager(models.Manager):
    def get_rules(self, user):
        return self.filter().order_by('-created_at')

    def get_rule(self, user, rule_id):
        return self.filter(id=rule_id, endpoint__service__user=user).last()

    def create_rule(self, endpoint, request_source, data_format, condition_field, condition_value, response_code,
                    response_body, is_active):
        return self.create(endpoint=endpoint, request_source=request_source, data_format=data_format,
                           condition_field=condition_field, condition_value=condition_value,
                           response_code=response_code, response_body=response_body, is_active=is_active)

    def update_rule(self, rule_id, request_source, data_format, condition_field, condition_value, response_code,
                    response_body, is_active):
        return self.filter(id=rule_id).update(request_source=request_source, data_format=data_format,
                                              condition_field=condition_field, condition_value=condition_value,
                                              response_code=response_code, response_body=response_body,
                                              is_active=is_active)
