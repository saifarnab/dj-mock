from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from helpers import auth_utils
from .models import MockEndpoint


class MockServiceView(APIView):
    """
    Dynamically handles GET, POST, PUT, DELETE, etc. requests
    for mocked services.
    """

    permission_classes = []
    authentication_classes = []

    @staticmethod
    def _invalid_path_response():
        err = {
            "code": "IPR404",
            "message": "Invalid path, Check endpoints",
            "lang": "en",
            "data": {}
        }
        return Response(err, status=status.HTTP_404_NOT_FOUND)

    def handle_request(self, request, service_base=None, endpoint_path=None, *args, **kwargs):
        # Clean input paths
        if service_base:
            service_base = str(service_base).strip('/').strip()
        if endpoint_path:
            endpoint_path = str(endpoint_path).strip('/').strip()

        print('service_base:', service_base)
        print('endpoint_path:', endpoint_path)

        # check endpoints
        try:
            endpoint = MockEndpoint.objects.get(
                service__base_path=service_base,
                path=endpoint_path,
                method=request.method
            )
        except MockEndpoint.DoesNotExist:
            return self._invalid_path_response()

        # handle auth
        auth_error = auth_utils.check_auth(request, endpoint)
        if auth_error:
            return auth_error

        return Response(endpoint.default_response, status=endpoint.default_http_status)

    # Dynamically route all HTTP methods to handle_request
    def get(self, request, *args, **kwargs):
        return self.handle_request(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.handle_request(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.handle_request(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.handle_request(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.handle_request(request, *args, **kwargs)
