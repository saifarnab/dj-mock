from django.db import models
from django.contrib.auth.models import User


class BasicAuthConfig(models.Model):
    endpoint = models.OneToOneField("MockEndpoint", on_delete=models.CASCADE, related_name="basic_auth")
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)


class JWTAuthConfig(models.Model):
    endpoint = models.OneToOneField("MockEndpoint", on_delete=models.CASCADE, related_name="jwt_auth")
    verify_key = models.TextField()  # public key


class ApiKeyAuthConfig(models.Model):
    endpoint = models.OneToOneField("MockEndpoint", on_delete=models.CASCADE, related_name="apikey_auth")
    header_name = models.CharField(max_length=100, default="Authorization")
    key_value = models.CharField(max_length=255)


class MockService(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="services")
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    base_path = models.CharField(max_length=255)  # e.g. "/banking"
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
    path = models.CharField(max_length=255)  # e.g. "/accounts"
    method = models.CharField(max_length=10, choices=HTTP_METHOD_CHOICES)
    require_auth = models.BooleanField(default=False)
    auth_type = models.CharField(max_length=20,
                                 choices=[("none", "None"), ("basic", "Basic"), ("api_key", "Api Key"), ("jwt", "JWT")],
                                 default="none")


class MockRule(models.Model):
    endpoint = models.ForeignKey(MockEndpoint, on_delete=models.CASCADE, related_name="rules")
    condition_field = models.CharField(max_length=100)  # e.g. "account_id"
    condition_value = models.CharField(max_length=100)  # e.g. "101"
    response_body = models.JSONField()
    response_code = models.IntegerField(default=200)
