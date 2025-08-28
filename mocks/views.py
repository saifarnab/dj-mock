# mocks/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import MockEndpoint
from helpers import auth_utils


class MockServiceView(APIView):
    def dispatch(self, request, *args, **kwargs):
        service_base = kwargs.get("service_base")  # e.g. banking
        endpoint_path = kwargs.get("endpoint_path")  # e.g. accounts

        try:
            endpoint = MockEndpoint.objects.get(
                service__base_path=f"/{service_base}",
                path=f"/{endpoint_path}",
                method=request.method
            )
        except MockEndpoint.DoesNotExist:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        # 🔹 Auth check (delegated to auth_utils)
        auth_error = auth_utils.check_auth(request, endpoint)
        if auth_error:
            return auth_error

        # 🔹 Match request data to rules
        req_data = request.query_params.dict()
        if request.data:
            req_data.update(request.data)

        for rule in endpoint.rules.all():
            if req_data.get(rule.condition_field) == rule.condition_value:
                return Response(rule.response_body, status=rule.response_code)

        return Response({"error": "No matching rule"}, status=404)
