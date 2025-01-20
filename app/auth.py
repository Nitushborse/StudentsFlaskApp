from .models import db, Staff
from datetime import datetime, timedelta
from flask import jsonify
import bcrypt
import jwt


SECRET_KEY = "may_secret_key"

def create_tokens(staff_id):
    access_token = jwt.encode(
        {"id": staff_id, "exp": datetime.utcnow() + timedelta(minutes=30)}, 
        SECRET_KEY, 
        algorithm="HS256"
    )
    refresh_token = jwt.encode(
        {"id": staff_id, "exp": datetime.utcnow() + timedelta(days=7)}, 
        SECRET_KEY, 
        algorithm="HS256"
    )
    return access_token, refresh_token

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
    accessToken, refreshToken = create_tokens(name)

    new_user = Staff(
        name = name,
        email = email,
        password=hashed_password.decode('utf-8'),
        accessToken = accessToken,
        refreshToken = refreshToken
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

    return jsonify({
        "accessToken": user.accessToken,
        "refreshToken": user.refreshToken,
        "user": user.to_dict()
    }), 200



