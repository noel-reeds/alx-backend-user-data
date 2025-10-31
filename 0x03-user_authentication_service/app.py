#!/usr/bin/env python3
"""Application module"""
from flask import Flask, jsonify, request, abort, make_response, redirect
from auth import Auth

app = Flask(__name__)
auth = Auth()


@app.route("/", methods=['GET'], strict_slashes=False)
def status():
    """Status of application"""
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users():
    """Register a user"""
    try:
        email = request.form.get("email", None)
        password = request.form.get("password", None)
        user = auth.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError as e:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """Logs in a user"""
    try:
        email = request.form.get("email", None)
        password = request.form.get("password", None)
        valid_credentials = auth.valid_login(email, password)
        if not valid_credentials:
            raise ValueError
        session_id = auth.create_session(email)
        _resp = make_response({"email": email, "message": "logged in"})
        _resp.set_cookie("session_id", session_id)
        return _resp
    except Exception as e:
        abort(401)


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout():
    """Logs out an active user"""
    try:
        session_id = request.cookies.get("session_id")
        if not session_id:
            raise ValueError
        user = auth.get_user_from_session_id(session_id)
        if user:
            auth.destroy_session(user.id)
            return redirect("/")
        else:
            abort(403)
    except Exception as e:
        abort(403)


@app.route("/profile", methods=['GET'], strict_slashes=False)
def profile():
    """User profile"""
    session_id = request.cookies.get("session_id")
    if not session_id:
        abort(403)
    user = auth.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": user.email}), 200
    abort(403)


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token():
    """Get reset password token"""
    try:
        email = request.form.get("email")
        # create a session to see if user exists
        session_id = auth.create_session(email)
        if not session_id:
            abort(403)
        reset_token = auth.get_reset_password_token(email)
        return jsonify({
            "email": email,
            "reset_token": reset_token
            }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
