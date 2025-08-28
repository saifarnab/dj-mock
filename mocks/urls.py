# mocks/urls.py
from django.urls import re_path
from .views import MockServiceView

urlpatterns = [
    re_path(r'^(?P<service_base>[^/]+)/(?P<endpoint_path>.+)$', MockServiceView.as_view()),
]
