from django.db import models
from django.contrib.auth.models import User


class BasicAuthConfig(models.Model):
    endpoint = models.OneToOneField("MockEndpoint", on_delete=models.CASCADE, related_name="basic_auth")
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class JWTAuthConfig(models.Model):
    endpoint = models.OneToOneField("MockEndpoint", on_delete=models.CASCADE, related_name="jwt_auth")
    auth_header = models.CharField(null=False, blank=False, default="Bearer")
    token = models.TextField(null=False, blank=False)


class ApiKeyAuthConfig(models.Model):
    ADD_TO = [
        ("header", "Header"),
        ("query_params", "Query Params")
    ]
    endpoint = models.OneToOneField("MockEndpoint", on_delete=models.CASCADE, related_name="apikey_auth")
    add_to = models.CharField(max_length=50, choices=ADD_TO, null=False, blank=False)
    key_name = models.CharField(max_length=100, default="API_KEY")
    key_value = models.CharField(max_length=255)


class MockService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    base_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

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
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=10, choices=HTTP_METHOD_CHOICES)
    default_response = models.JSONField(null=False, blank=False)
    default_http_status = models.IntegerField(null=False, blank=False)
    auth_type = models.CharField(max_length=20,
                                 choices=[("none", "None"), ("basic", "Basic"), ("api_key", "Api Key"), ("jwt", "JWT")],
                                 default="none")

    def __str__(self):
        return f'{self.service.name}:{self.service.base_path}/{self.path}'


class MockRule(models.Model):
    endpoint = models.ForeignKey(MockEndpoint, on_delete=models.CASCADE, related_name="rules")
    condition_field = models.CharField(max_length=100)
    condition_value = models.CharField(max_length=100)
    response_body = models.JSONField()
    response_code = models.IntegerField(default=200)
