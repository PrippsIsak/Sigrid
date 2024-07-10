from main import DATABASE

COLLECTION_USER = 'User'

def login(username, password):
    """Function looks if a user exist and if correct password matches"""
    try:
        collection = DATABASE.get_collection(COLLECTION_USER)
        user = collection.find_one({'Username' : username})
        if user['password'] == password:
            return 'OK'
     
    except Exception as e:
        return e
    
    return 'NOT OK'