#!/usr/bin/env python3
import bcrypt


def _hash_password(password: str) -> bytes:
    """Hashes a password into bytes"""
    hashed_passwd = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    return hashed_passwd
