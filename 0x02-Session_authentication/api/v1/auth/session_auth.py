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
        if type(user_id) is not str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves user_id for the session_id"""
        if not session_id:
            return None
        if type(session_id) is not str:
            return None
        return self.user_id_by_session_id.get(session_id)
