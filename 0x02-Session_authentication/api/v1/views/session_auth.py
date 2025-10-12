#!/usr/bin/env python3
"""New view for Session Authentication"""
import os
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def view_for_session_auth():
    """POST /api/v1/auth_session/login
    Return:
      - User based on parameters or error
    """
    keys = ("email", "password")
    credentials = {key: request.form.get(key) for key in keys}
    for k, v in credentials.items():
        if v == "" or v is None:
            return jsonify({"error": f"{k} missing"}), 400
    try:
        users = User.search({"email": credentials.get("email")})
        if not users:
            return jsonify({"error": "no user found for this email"}), 404
        for user in users:
            if not user.is_valid_password(credentials.get("password")):
                return jsonify({"error": "wrong password"}), 401
        from api.v1.app import auth
        user = next(iter(users))
        _my_session_id = auth.create_session(user.id)
        session_k = os.environ.get("SESSION_NAME")
        user = jsonify(user.to_json())
        user.set_cookie(session_k, _my_session_id)
        return user
    except Exception as e:
        return None
