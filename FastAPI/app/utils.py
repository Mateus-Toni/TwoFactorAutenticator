from datetime import datetime, timedelta
from random import randint
import logging

from passlib.context import CryptContext
from jose import jwt, JWTError

from parameters import ACCESS_TOKEN_EXPIRE, SECRET_KEY, ALGORITHM
from dao.user_dao import UserDb

crypt = CryptContext(schemes=['bcrypt'])

def get_pwd_hash(password):

    return crypt.hash(password)


def check_pwd_hash(password_hash, password):

    return crypt.verify(password, password_hash)
