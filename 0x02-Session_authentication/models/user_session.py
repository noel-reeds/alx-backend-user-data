#!/usr/bin/env python3
"""Sessions in database"""
from models.base import Base


class UserSession(Base):
    """Implements sessions in database"""
    def __init__(self, *args: list, **kwargs: dict):
        """Initialize a UserSession instance"""
        super().__init__(*args, **kwargs)
        self.email = kwargs.get('email')
        self._password = kwargs.get('_password')
        self.first_name = kwargs.get('first_name')
        self.last_name = kwargs.get('last_name')
        if args:
            self.user_id = args[0]
            self.session_id = args[1]
        else:
            self.user_id = kwargs.get('user_id')
            self.session_id = kwargs.get('session_id')
