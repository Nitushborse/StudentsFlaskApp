from .models import db, Staff
from datetime import datetime, timedelta
from flask import jsonify, request
import bcrypt
import jwt
from dotenv import load_dotenv
import os
from .check_token import token_required

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

def create_tokens(staff_id):
    access_token = jwt.encode(
        {
            "id": staff_id,
            "type": "access",
            "exp": datetime.utcnow() + timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    refresh_token = jwt.encode(
        {
            "id": staff_id,
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7)
        },
        SECRET_KEY,
        algorithm="HS256"
    )

    return access_token, refresh_token


@token_required
def Create_new_user(data):
    if not data:
        return jsonify({"error" : "Data is required"}), 400

    if "name" not in data or "email" not in data or "password" not in data:
        return jsonify({"error":"name, email, password are requared"}), 400
    
    name = data['name']
    email = data['email']
    password = data['password']

    if Staff.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    # accessToken, refreshToken = create_tokens(name)

    new_user = Staff(
        name = name,
        email = email,
        password=hashed_password.decode('utf-8'),
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "Staff registered successfully",
        "user":new_user.to_dict()
    }
    ), 201

def Login(data):
    if not data:
        return jsonify({"error" : "Missing body in requast"}), 400
    
    if 'username' not in data or 'password' not in data:
        return jsonify({"error" : "username or password is missing in data"}), 400
    
    username = data['username']
    passwo = data['password'] 

    user = Staff.query.filter_by(email=username).first()

    if not user or not bcrypt.checkpw(passwo.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"error": "Invalid username or password"}), 401
    
    accessToken, refreshToken = create_tokens(user.id)
    user.refreshToken = refreshToken

    db.session.commit()

    return jsonify({
        "accessToken": accessToken,
        "refreshToken": refreshToken,
        "user": user.to_dict()
    }), 200

def Refresh_access_token(data):
    if not data or "refreshToken" not in data:
        return jsonify({"error": "Refresh token is required"}), 400

    refresh_token = data["refreshToken"]

    try:
        decoded = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])

        if decoded.get("type") != "refresh":
            return jsonify({"error": "Invalid refresh token"}), 401

        user = Staff.query.get(decoded["id"])

        if not user or user.refreshToken != refresh_token:
            return jsonify({"error": "Refresh token mismatch"}), 401

        new_access_token, new_refresh_token = create_tokens(user.id)

        user.refreshToken = new_refresh_token

        return jsonify({
            "accessToken": new_access_token
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Refresh token expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid refresh token"}), 401


@token_required
def Logout():
    user_id = request.user["id"]

    user = Staff.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Invalidate refresh token
    user.refreshToken = None
    # user.isLoggedOut = True

    db.session.commit()

    return jsonify({
        "message": "Logged out successfully"
    }), 200
