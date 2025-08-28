from django.contrib import admin
from .models import (
    MockService,
    MockEndpoint,
    MockRule,
    BasicAuthConfig,
    JWTAuthConfig,
    ApiKeyAuthConfig,
)


class MockRuleInline(admin.TabularInline):
    model = MockRule
    extra = 1


class BasicAuthConfigInline(admin.StackedInline):
    model = BasicAuthConfig
    extra = 0
    max_num = 1


class JWTAuthConfigInline(admin.StackedInline):
    model = JWTAuthConfig
    extra = 0
    max_num = 1


class ApiKeyAuthConfigInline(admin.StackedInline):
    model = ApiKeyAuthConfig
    extra = 0
    max_num = 1


@admin.register(MockEndpoint)
class MockEndpointAdmin(admin.ModelAdmin):
    list_display = ("id", "service", "path", "method", "auth_type")
    list_filter = ("method", "auth_type")
    search_fields = ("path", "service__name")
    inlines = [MockRuleInline, BasicAuthConfigInline, JWTAuthConfigInline, ApiKeyAuthConfigInline]


@admin.register(MockService)
class MockServiceAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "base_path", "user", "created_at")
    search_fields = ("name", "base_path", "user__username")
    list_filter = ("created_at",)


@admin.register(MockRule)
class MockRuleAdmin(admin.ModelAdmin):
    list_display = ("id", "endpoint", "condition_field", "condition_value", "response_code")
    search_fields = ("condition_field", "condition_value")


# Optional: register auth configs separately (if you want them outside endpoints)
@admin.register(BasicAuthConfig)
class BasicAuthConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "endpoint", "username")


@admin.register(JWTAuthConfig)
class JWTAuthConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "endpoint")


@admin.register(ApiKeyAuthConfig)
class ApiKeyAuthConfigAdmin(admin.ModelAdmin):
    list_display = ("id", "endpoint", "header_name", "key_value")
