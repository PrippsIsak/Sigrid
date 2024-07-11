from extensions import CRYPT

def hash_password(password):
    hashed_password = CRYPT.generate_password_hash(password).decode('uft-8')
    return CRYPT.check_password_hash(hashed_password, password)

def check_password(plain_password, hashed_password):
    return CRYPT.check_password_hash(plain_password.encode('utf-8'), hash_password)