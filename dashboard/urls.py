from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('services', views.service_list_view, name='service_list'),
    path('endpoints', views.endpoint_list_view, name='endpoint_list'),
    path('basic-auths', views.basic_auth_list_view, name='basic_auth_list'),
    path('api-key-auths', views.api_key_auth_list_view, name='api_key_auth_list'),
    path('jwt-auths', views.jwt_auth_list_view, name='jwt_auth_list'),
    path('rules', views.rule_list_view, name='rule_list'),
    path('create-rule', views.create_rule_view, name='create_rule'),
    path('create-service', views.create_service_view, name='create_service'),
    path('create-endpoint', views.create_endpoint_view, name='create_endpoint'),
    path('create-basic-auth', views.create_basic_auth_view, name='create_basic_auth'),
    path('create-api-key-auth', views.create_api_key_auth_view, name='create_api_key_auth'),
    path('create-jwt-auth', views.create_jwt_auth_view, name='create_jwt_auth'),
    path('edit-service/<int:service_id>', views.edit_service_view, name='edit_service'),
    path('edit-endpoint/<int:endpoint_id>', views.edit_endpoint_view, name='edit_endpoint'),
    path('edit-basic-auth/<int:basic_auth_id>', views.edit_basic_auth_view, name='edit_basic_auth'),
    path('edit-api-key-auth/<int:api_key_auth_id>', views.edit_api_key_auth_view, name='edit_api_key_auth'),
    path('edit-jwt-auth/<int:jwt_auth_id>', views.edit_jwt_auth_view, name='edit_jwt_auth'),
    path('edit-rule/<int:rule_id>', views.edit_rule_view, name='edit_rule'),
    path('details-service/<int:service_id>', views.details_service_view, name='details_service'),
    path('details-endpoint/<int:endpoint_id>', views.details_endpoint_view, name='details_endpoint'),
    path('details-basic-auth/<int:basic_auth_id>', views.details_basic_auth_view, name='details_basic_auth'),
    path('details-api-key-auth/<int:api_key_auth_id>', views.details_api_key_auth_view, name='details_api_key_auth'),
    path('details-jwt-auth/<int:jwt_auth_id>', views.details_jwt_auth_view, name='details_jwt_auth'),
    path('details-rule/<int:rule_id>', views.details_rule_view, name='details_rule'),

]
