#!/usr/bin/env python3
"""Basic Auth. module"""
import re
import base64
from models.user import User
from typing import TypeVar
from .auth import Auth


class BasicAuth(Auth):
    """Basic Auth. class"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """Extracts- Base64 part of Auth Header"""
        if not authorization_header or type(authorization_header) != str:
            return None
        try:
            assert authorization_header.startswith("Basic")
            assert re.match(r'\b\w+\s', authorization_header)
            return authorization_header.split(" ")[1]
        except Exception as e:
            return None

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """Decodes Base64 Auth. Header"""
        if not base64_authorization_header:
            return None
        if type(base64_authorization_header) != str:
            return None
        try:
            d = base64.b64decode(base64_authorization_header.encode())
            assert base64.b64encode(d) == base64_authorization_header.encode()
            return d.decode("utf-8")
        except Exception as e:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """Extracts user credentials"""
        if not decoded_base64_authorization_header:
            return (None, None)
        if type(decoded_base64_authorization_header) != str:
            return (None, None)
        try:
            authorization_header = decoded_base64_authorization_header
            # match for exactly one ":" in auth header
            # assert re.match(r'^[^:]+:[.*]+$', authorization_header)
            creds = decoded_base64_authorization_header.split(":", maxsplit=1)
            return tuple(creds)
        except Exception as e:
            return (None, None)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """User interface from user email and passwd"""
        if not user_email or type(user_email) != str:
            return None
        if not user_pwd or type(user_pwd) != str:
            return None
        try:
            users = User.search({"email": user_email})
            if not users:
                return None
            for user in users:
                if not user.is_valid_password(user_pwd):
                    return None
            return users
        except Exception as e:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Overloads Auth and retrieves the User instance for a request"""
        auth_header = self.authorization_header(request)
        base64_auth = self.extract_base64_authorization_header(auth_header)
        decoded_auth = self.decode_base64_authorization_header(base64_auth)
        user_pwd = self.extract_user_credentials(decoded_auth)
        user = self.user_object_from_credentials(*user_pwd)
        return user
