from main import DATABASE
from pymongo import errors

COLLECTION_USER = 'User'

def get_user(username):
    """Find user on username and return it"""
    try:
        collection = DATABASE.get_collection(COLLECTION_USER)
        user = collection.find_one({'Username': username})
        if user is None:
            return None, None
    except errors.PyMongoError as err:
        return None, err
    
    return user, None

def create_user(username, password):
    try:
        collection = DATABASE.get_collection(COLLECTION_USER)
        result = collection.find_one({'Username': username})
        if result is None:
            errors.InvalidName
        
        result = collection._insert_one({'Username': username, 'Password': password})
        return None
    except errors.PyMongoError as err:
        return  err 