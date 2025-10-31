#!/usr/bin/env python3
"""Application module"""
from flask import Flask, jsonify, request, abort, make_response
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
            abort(401)
        session_id = auth.create_session(email)
        _resp = make_response({"email": email, "message": "logged in"})
        _resp.set_cookie("session_id", session_id)
        return _resp
    except Exception as e:
        return None


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
