#!/usr/bin/env python3
"""Basic Auth. module"""
import re
from .auth import Auth


class BasicAuth(Auth):
    """Basic Auth. class"""
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Extracts- Base64 part of Auth Header"""
        if not authorization_header or type(authorization_header) != str:
            return None
        try:
            assert authorization_header.startswith("Basic")
            assert re.match(r'\b\w+\s', authorization_header)
            return authorization_header.split(" ")[1]
        except Exception as e:
            return None
