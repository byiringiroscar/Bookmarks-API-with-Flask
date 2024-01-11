from os import access
from flask import Blueprint, jsonify



auth = Blueprint("auth", __name__, url_prefix='/api/v1/auth')



@auth.post('/register')
def register():
    return jsonify({"message": "register created"})



@auth.get('/me')
def me():
    return jsonify({"message": "me created"})
