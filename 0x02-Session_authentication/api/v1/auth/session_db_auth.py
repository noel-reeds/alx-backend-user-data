#!/usr/bin/env python3
"""Sessions in DB Auth."""
from models.user_session import UserSession
from api.v1.auth.session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    """Implements SessionDBAuth methods"""
    def create_session(self, user_id=None):
        """creates and stores new instance of UserSession"""
        session_id = super().create_session(user_id)
        if not session_id:
            return None
        try:
            user_session = UserSession(*[user_id, session_id])
            user_session.save()
        except Exception as e:
            return None
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the User ID based on session_id"""
        if not session_id:
            return None
        try:
            UserSession.load_from_file()
            attrs = {"session_id": session_id}
            user = next(iter(UserSession.search(attrs)))
            if user:
                return user.user_id
            return None
        except Exception as e:
            return None

    def destroy_session(self, request=None):
        """destroys the UserSession based on the session_id"""
        super().__init__()
        if not request:
            return False
        session_id = self.session_cookie(request)
        if not session_id:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False
        del self.user_id_by_session_id[session_id]
        UserSession(self).remove()
        return True
