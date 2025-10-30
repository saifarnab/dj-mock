# mocks/auth_utils.py
import base64
import json

from rest_framework.response import Response


def check_auth(request, endpoint):
    """Validate auths based on endpoint.auth_type"""
    if endpoint.auth_type == "none":
        return None  # no error

    elif endpoint.auth_type == "basic":
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Basic "):
            return Response(json.loads(endpoint.service.basic_auth.failed_response),
                            status=endpoint.service.basic_auth.failed_http_status)
        encoded = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)

        if not (endpoint.service.basic_auth.username == username and endpoint.service.basic_auth.password == password):
            return Response(json.loads(endpoint.service.basic_auth.failed_response),
                            status=endpoint.service.basic_auth.failed_http_status)

    elif endpoint.auth_type == "jwt":
        token = request.headers.get("Authorization", "").strip()
        if not token:
            # return Response({"error": "Missing JWT token"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(json.loads(endpoint.service.jwt_auth.failed_response),
                            status=endpoint.service.jwt_auth.failed_http_status)

        if str(token).split(' ')[0].lower() != endpoint.auth_type.lower():
            # return Response({"error": "Invalid auths header"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(json.loads(endpoint.service.jwt_auth.failed_response),
                            status=endpoint.service.jwt_auth.failed_http_status)
        try:
            if str(token).split(' ')[1] != endpoint.service.jwt_auth.token:
                # return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
                return Response(json.loads(endpoint.service.jwt_auth.failed_response),
                                status=endpoint.service.jwt_auth.failed_http_status)
        except Exception as e:
            # return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
            return Response(json.loads(endpoint.service.jwt_auth.failed_response),
                            status=endpoint.service.jwt_auth.failed_http_status)


    elif endpoint.auth_type == "api_key":
        if endpoint.service.api_key.add_to == 'header':
            key_name = endpoint.service.api_key.key_name
            key_value = request.headers.get(key_name)
            if key_value != endpoint.service.api_key.key_value:
                # return Response({"error": "Invalid API Key"}, status=status.HTTP_401_UNAUTHORIZED)
                return Response(json.loads(endpoint.service.api_key.failed_response),
                                status=endpoint.service.api_key.failed_http_status)

        elif endpoint.service.api_key.add_to == 'query_params':
            key_name = endpoint.service.api_key.key_name
            key_value = request.query_params.get(key_name)
            if key_value != endpoint.service.api_key.key_value:
                # return Response({"error": "Invalid API Key"}, status=status.HTTP_401_UNAUTHORIZED)
                return Response(json.loads(endpoint.service.api_key.failed_response),
                                status=endpoint.service.api_key.failed_http_status)

        elif endpoint.service.api_key.add_to == 'body':
            try:
                body = request.data
                key_name = endpoint.service.api_key.key_name
                key_value = body.get(key_name)
                if key_value != endpoint.service.api_key.key_value:
                    return Response(
                        json.loads(endpoint.service.api_key.failed_response),
                        status=endpoint.service.api_key.failed_http_status
                    )
            except Exception:
                return Response(
                    json.loads(endpoint.service.api_key.failed_response),
                    status=endpoint.service.api_key.failed_http_status
                )

    return None  # ✅ auths passed
