#!/usr/bin/env python3
"""Auth. module"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth. class"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require auth."""
        if not path or not excluded_paths or len(excluded_paths) == 0:
            return True
        for _path in excluded_paths:
            if _path.endswith("*") and _path.rstrip("*") in path:
                return False
            path = path.strip('/')
            excluded_paths[excluded_paths.index(_path)] = _path.strip('/')
        if path not in excluded_paths:
            return True
        if path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """Auth. Header"""
        if not request:
            return None
        if request.headers.get("Authorization") is None:
            return None
        return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None

    def session_cookie(self, request=None):
        """Returns a cookie value from a request"""
        if not request:
            return None
        _my_session_id = request.cookies.get("_my_session_id")
        return _my_session_id
