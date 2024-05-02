from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from VendorManagement.settings import TOKENS

def check_token(request):
    bearer_token = request.headers.get('Authorization') # getting token
    if not bearer_token:
        raise AuthenticationFailed('Authorization header missing.')

    try:
        token = bearer_token.split()[1]  # Get the token (excluding 'Bearer')
    except IndexError:
        raise AuthenticationFailed('Invalid token format. Bearer token required.')

    if token not in TOKENS:
        raise AuthenticationFailed('Invalid token.')

    return True
