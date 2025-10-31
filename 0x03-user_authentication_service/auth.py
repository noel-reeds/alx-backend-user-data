#!/usr/bin/env python3
import bcrypt
import uuid
from typing import Optional
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """Hashes a password into bytes"""
    hashed_passwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_passwd


def _generate_uuid() -> str:
    """Generates UUIDs"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Registers a user"""
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError(f"User {user.email} already exists.")
        except NoResultFound as e:
            hashed = _hash_password(password)
            new_user = self._db.add_user(email, hashed)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user credentials"""
        try:
            user = self._db.find_user_by(email=email)
            valid = bcrypt.checkpw(password.encode(), user.hashed_password)
            if user and valid:
                return True
            return False
        except NoResultFound as e:
            return False
        except Exception as e:
            return e

    def create_session(self, email: str) -> str:
        """Creates a session id for a user"""
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=_generate_uuid())
            return user.session_id
        except NoResultFound as e:
            return

    def get_user_from_session_id(self, session_id: str) -> Optional[str]:
        """Retrieve user from session id"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """Destroys a user session"""
        try:
            self._db.update_user(user_id, session_id=None)
            return None
        except ValueError as e:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate reset password token"""
        try:
            user = self._db.find_user_by(email=email)
            if not user:
                raise ValueError
            reset_token = _generate_uuid()
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except ValueError as e:
            return None
