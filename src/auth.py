from os import access
from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from src.constants.http_status_code import *
import validators
from src.database import User, db


auth = Blueprint("auth", __name__, url_prefix='/api/v1/auth')



@auth.post('/register')
def register():
    username = request.json['username']
    email = request.json['email']
    password = request.json['password']

    if len(password) < 6:
        return jsonify({"message": "password must be at least 6 characters"}), HTTP_400_BAD_REQUEST
    
    if len(username) <3:
        return jsonify({"message": "username must be at least 3 characters"}), HTTP_400_BAD_REQUEST
    
    if not username.isalnum() or " " in username:
        return jsonify({"message": "username must be alphanumeric, also no spaces"}), HTTP_400_BAD_REQUEST
    
    if not validators.email(email):
        return jsonify({"message": "email is not valid"}), HTTP_400_BAD_REQUEST
    
    
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"message": "email already exists"}), HTTP_409_CONFLICT
    
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"message": "username already exists"}), HTTP_409_CONFLICT
    
    pwd_hash = generate_password_hash(password)

    user = User(username=username, email=email, password=pwd_hash)
    db.session.add(user)
    db.session.commit()
    return jsonify({
        'message': 'User created',
         'user': {
             'username': username, 'email': email
         }
          }), HTTP_201_CREATED



@auth.get('/me')
def me():
    return jsonify({"message": "me created"})
