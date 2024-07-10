from flask import request, jsonify, Blueprint
from main import BCRYPT
import database as db

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    """Hash password and calls the dtaabase api"""
    data = request.get_json()
    if not data:
        return jsonify({'Error': 'Invalid input'})
    
    try:
        #TODO: hash password
        username = str(data.get('username', 0))
        password = str(data.get('password', 0))
        
    except(KeyError, ValueError):
        return jsonify({'Error': 'Invalid data'}), 400
    
    status = db.login(username, password)
    if status !='OK':
        return jsonify({'Error': 'Wrong password or username'}), 500

    return jsonify({'Succes': 'Login succesful'}), 200

@user_bp.route('/register', methods=['POST'])
def register():
    """Create a user """
    #TODO: fix
    data = request