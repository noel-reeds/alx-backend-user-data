#!/usr/bin/env python3
"""Basic Auth. module"""
import re
import base64
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
