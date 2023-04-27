from datetime import datetime, timedelta
from random import randint
import logging

from passlib.context import CryptContext
from jose import jwt

from parameters import ACCESS_TOKEN_EXPIRE, SECRET_KEY, ALGORITHM
from dao.user_dao import UserDb

crypt = CryptContext(schemes=['bcrypt'])

def get_pwd_hash(password):

    return crypt.hash(password)


def check_pwd_hash(password_hash, password):

    return crypt.verify(password, password_hash)


def two_auth_journey(id_user: int):

    code = randint(10000, 999999)
    UserDb.save_code_in_db(code=code, id_user=id_user)
    logging.info(code) #envia código no email

    payload = {
        'user_id': id_user,
        'exp': datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE),
        'type': 'code',
        'two_auth': False
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token