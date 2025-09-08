# mocks/auth_utils.py
import base64
import jwt
from rest_framework.response import Response
from rest_framework import status


def check_auth(request, endpoint):
    """Validate auth based on endpoint.auth_type"""
    if endpoint.auth_type == "none":
        return None  # no error

    elif endpoint.auth_type == "basic":
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Basic "):
            return Response({"error": "Missing Basic Auth"}, status=status.HTTP_401_UNAUTHORIZED)
        encoded = auth_header.split(" ")[1]
        decoded = base64.b64decode(encoded).decode("utf-8")
        username, password = decoded.split(":", 1)

        if not hasattr(endpoint, "basic_auth") or \
                endpoint.basic_auth.username != username or \
                endpoint.basic_auth.password != password:
            return Response({"error": "Invalid Basic Auth"}, status=status.HTTP_401_UNAUTHORIZED)

    elif endpoint.auth_type == "jwt":
        token = request.headers.get("Authorization", "")
        if not token:
            return Response({"error": "Missing JWT token"}, status=status.HTTP_401_UNAUTHORIZED)

        if str(token).split(' ')[0].lower() != endpoint.auth_type.lower():
            return Response({"error": "Invalid auth header"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            print(str(token).split(' ')[1].lower())
            if str(token).split(' ')[1] != endpoint.jwt_auth.token:
                return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({"error": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED)


    elif endpoint.auth_type == "api_key":
        if endpoint.apikey_auth.add_to == 'header':
            key_name = endpoint.apikey_auth.key_name
            key_value = request.headers.get(key_name)
            if key_value != endpoint.apikey_auth.key_value:
                return Response({"error": "Invalid API Key"}, status=status.HTTP_401_UNAUTHORIZED)

        elif endpoint.apikey_auth.add_to == 'query_params':
            key_name = endpoint.apikey_auth.key_name
            key_value = request.query_params.get(key_name)
            print(key_value)
            if key_value != endpoint.apikey_auth.key_value:
                return Response({"error": "Invalid API Key"}, status=status.HTTP_401_UNAUTHORIZED)

    return None  # ✅ auth passed
