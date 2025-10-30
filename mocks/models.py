from django.db import models
from django.contrib.auth.models import User

from mocks import managers


class MockService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    base_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = managers.MockServiceManager()

    def __str__(self):
        return self.name


class MockEndpoint(models.Model):
    HTTP_METHOD_CHOICES = [
        ("GET", "GET"),
        ("POST", "POST"),
        ("PUT", "PUT"),
        ("PATCH", "PATCH"),
        ("DELETE", "DELETE"),
        ("HEAD", "HEAD"),
        ("OPTIONS", "OPTIONS"),
    ]
    service = models.ForeignKey(MockService, on_delete=models.CASCADE, related_name="endpoints")
    endpoint_name = models.CharField(max_length=255)
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=HTTP_METHOD_CHOICES)
    default_response = models.JSONField(null=False, blank=False)
    default_http_status = models.IntegerField(null=False, blank=False)
    auth_type = models.CharField(max_length=20,
                                 choices=[("none", "None"), ("basic", "Basic"), ("api_key", "Api Key"), ("jwt", "JWT")],
                                 default="none")
    hit_count = models.BigIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = managers.MockEndpointManager()

    def __str__(self):
        return f'MockEndpoint:{self.service.base_path}/{self.path}'


class BasicAuthConfig(models.Model):
    service = models.OneToOneField("MockService", on_delete=models.CASCADE, related_name="basic_auth")
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    failed_http_status = models.IntegerField(default=401)
    failed_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = managers.BasicAuthConfigManager()

    def __str__(self):
        return self.username


class JWTAuthConfig(models.Model):
    service = models.OneToOneField("MockService", on_delete=models.CASCADE, related_name="jwt_auth")
    auth_header = models.CharField(null=False, blank=False, default="Bearer")
    token = models.TextField(null=False, blank=False)
    failed_http_status = models.IntegerField(default=401)
    failed_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = managers.JWTAuthConfigManager()

    def __str__(self):
        return f"{self.auth_header}-{self.service.name}"


class ApiKeyAuthConfig(models.Model):
    ADD_TO = [
        ("header", "Header"),
        ("query_params", "Query Params"),
        ("body", "Body")
    ]
    service = models.OneToOneField("MockService", on_delete=models.CASCADE, related_name="api_key")
    add_to = models.CharField(max_length=50, choices=ADD_TO, null=False, blank=False)
    key_name = models.CharField(max_length=100, default="API_KEY")
    key_value = models.CharField(max_length=255)
    failed_http_status = models.IntegerField(default=401)
    failed_response = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = managers.APIKeyAuthConfigManager()

    def __str__(self):
        return self.key_name


class MockRule(models.Model):
    REQUEST_SOURCES = [
        ("PAYLOAD", "PAYLOAD"),
        ("QUERY_PARAMS", "QUERY PARAMS")
    ]
    DATA_FORMAT = [
        ("JSON", "JSON"),
        ("XML", "XML")
    ]
    endpoint = models.ForeignKey(MockEndpoint, on_delete=models.CASCADE, related_name="rules")
    request_source = models.CharField(max_length=50, choices=REQUEST_SOURCES, null=False, blank=False)
    data_format = models.CharField(max_length=50, choices=DATA_FORMAT, null=False, blank=False)
    condition_field = models.CharField(max_length=100)
    condition_value = models.CharField(max_length=100)
    response_body = models.JSONField()
    response_code = models.IntegerField(default=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    objects = managers.MockRuleManager()

    def __str__(self):
        return f'MockRule:{self.endpoint.service.base_path}/{self.endpoint.path}'
