import json
import xml.etree.ElementTree as ET
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_xml.parsers import XMLParser
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from helpers import auth_utils, utils
from helpers.utils import demo
from .models import MockEndpoint, MockRule


class MockServiceView(APIView):
    """
    Dynamically handles GET, POST, PUT, DELETE, etc. requests
    for mocked services.
    """

    permission_classes = []
    authentication_classes = []
    parser_classes = [JSONParser, XMLParser, FormParser, MultiPartParser]

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

        # check endpoints
        try:
            endpoint = MockEndpoint.objects.get(
                service__base_path=service_base,
                path=endpoint_path,
                method=request.method
            )
        except MockEndpoint.DoesNotExist:
            return self._invalid_path_response()

        # increase hit count
        MockEndpoint.objects.increase_hit_count(endpoint.id)

        # handle auths
        auth_error = auth_utils.check_auth(request, endpoint)
        if auth_error:
            return auth_error

        # check mock rules
        mock_rules = MockRule.objects.filter(endpoint=endpoint)
        if mock_rules:
            for mock_rule in mock_rules:
                if mock_rule.request_source == "PAYLOAD":
                    if mock_rule.data_format == "JSON":
                        value = utils.json_value_by_key(request.data, mock_rule.condition_field)
                        if str(value) == str(mock_rule.condition_value):
                            jsonify = json.loads(mock_rule.response_body)
                            return Response(jsonify, status=mock_rule.response_code)
                    elif mock_rule.data_format == "XML":
                        try:
                            root = ET.fromstring(request.body.decode('utf-8'))
                            value = utils.xml_value_by_tag(root, mock_rule.condition_field)
                            if str(value) == str(mock_rule.condition_value):
                                response_body = mock_rule.response_body
                                return Response(response_body, status=mock_rule.response_code,
                                                content_type="application/xml")
                        except ET.ParseError:
                            return Response(
                                {"error": "Invalid XML format"},
                                status=400
                            )
                elif mock_rule.request_source == "QUERY_PARAMS":
                    value = request.query_params.get(mock_rule.condition_field)
                    if str(value) == str(mock_rule.condition_value):
                        if mock_rule.data_format == "JSON":
                            jsonify = json.loads(mock_rule.response_body)
                            return Response(jsonify, status=mock_rule.response_code)
                        elif mock_rule.data_format == "XML":
                            return Response(
                                mock_rule.response_body,
                                status=mock_rule.response_code,
                                content_type="application/xml"
                            )

        jsonify = json.loads(endpoint.default_response)
        return Response(jsonify, status=endpoint.default_http_status)

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
