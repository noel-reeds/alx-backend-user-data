#!/usr/bin/env python3
"""Session Auth. Expiration"""
import os
import datetime as dt
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Implements Session Auth. Expiration"""
    def __init__(self):
        """Initialize Session Auth. instance"""
        try:
            s_d = os.environ.get("SESSION_DURATION")
            self.session_duration = int(s_d) if s_d.isdecimal() else None
            if not self.session_duration:
                raise Exception
        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a session"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        try:
            self.user_id_by_session_id[session_id] = {}
            self.user_id_by_session_id[session_id]["user_id"] = user_id
            self.user_id_by_session_id[session_id]["created_at"] = \
                dt.datetime.now()
        except Exception as e:
            return None
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Retrieves user_id for the session_id"""
        if not session_id:
            return None
        if session_id not in self.user_id_by_session_id:
            return None
        user_id = self.user_id_by_session_id.get(session_id).get("user_id")
        if self.session_duration <= 0:
            return user_id
        created_at = self.user_id_by_session_id.get(
                session_id).get("created_at")
        if not created_at:
            return None
        td = dt.timedelta(seconds=self.session_duration)
        if created_at + td < dt.datetime.now():
            return None
        return user_id
