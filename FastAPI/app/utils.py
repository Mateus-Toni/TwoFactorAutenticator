from passlib.context import CryptContext

crypt = CryptContext(schemes=['bcrypt'])

def get_pwd_hash(password):

    hash_password = crypt.hash(password)

    return hash_password