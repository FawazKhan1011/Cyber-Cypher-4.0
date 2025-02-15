from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo

def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = mongo.db.users.find_one({"username": username})
    if user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    mongo.db.users.insert_one({"username": username, "password": hashed_password})

    return jsonify({"message": "User registered successfully"}), 201

def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user = mongo.db.users.find_one({"username": username})
    if not user or not check_password_hash(user['password'], password):
        return jsonify({"error": "Invalid credentials"}), 401

    return jsonify({"message": "Logged in successfully"}), 200