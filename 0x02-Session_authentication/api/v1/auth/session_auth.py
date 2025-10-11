#!/usr/bin/env python3
"""Session module"""
import uuid
from api.v1.auth.auth import Auth


class SessionAuth(Auth):
    """Session Authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session id for a user_id"""
        if not user_id:
            return None
        if type(user_id) != str:
            return None
        session_id = uuid.uuid4()
        user_id_by_session_id[session_id] = user_id
        return session_id
