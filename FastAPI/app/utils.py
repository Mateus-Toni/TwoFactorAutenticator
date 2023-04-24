from passlib.context import CryptContext

crypt = CryptContext(schemes=['bcrypt'])

def get_pwd_hash(password):

    return crypt.hash(password)

def check_pwd_hash(password_hash, password):

    return crypt.verify(password, password_hash)