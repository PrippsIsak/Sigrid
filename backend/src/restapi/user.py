from flask import request, jsonify, Blueprint
from util.hashing import hash_password, check_password 
import database.user as db
from pymongo import errors

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    """Hash password and calls the dtaabase api"""
    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Invalid input'})
    
    username = str(data['username'])
    password = str(data['password'])

    user, err = db.get_user(username)
    if err is None:
        return jsonify({'Error': 'Internal server error'}), 500
    
    if user != None and check_password(password, user['password']):
        return jsonify({'Succes': 'Login succesful'}), 200
    return jsonify({'Error', 'Wrong username or passsword'}), 400

@user_bp.route('/register', methods=['POST'])
def register():
    """Create a user """
    data = request.get_json()
    username = str(data['username'])
    password = str(data['password'])
    hashed_password = hash_password(password)

    err = db.create_user(username, hashed_password)
    
    if err != None:
         if err == errors.InvalidName:
            return jsonify({'Error', 'User Already exist'}), 400
         return ({'Error': 'Internal server error'}), 500
    return ({'Succes': 'User created'}, 200)
