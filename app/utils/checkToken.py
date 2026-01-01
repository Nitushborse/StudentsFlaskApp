from flask import request, jsonify
import jwt
from functools import wraps
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
# Secret key for JWT
SECRET_KEY = os.getenv('SECRET_KEY')

# Decorator to check for a valid token
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get("Authorization")

        if not auth_header or not auth_header.startswith("Bearer "):
            return jsonify({"error": "Token is missing"}), 401

        token = auth_header.split(" ")[1]

        try:
            decoded_data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            if decoded_data.get("type") != "access":
                return jsonify({"error": "Invalid access token"}), 401

            request.user = decoded_data

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated