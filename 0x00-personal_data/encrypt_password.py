#!/usr/bin/env python3
"""encrypts a password"""
import bcrypt


def hash_password(password: str) -> bytes:
    """hashes a passwd str to a byte str"""
    passwd = password.encode('utf-8')
    hashed_passwd = bcrypt.hashpw(passwd, bcrypt.gensalt())
    return hashed_passwd
