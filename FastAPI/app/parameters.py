import os
from dotenv import load_dotenv

load_dotenv()

#JWT
SECRET_KEY = os.environ.get('SECRET_KEY')
ALGORITHM = os.environ.get('ALGORITHM')
ACCESS_TOKEN_EXPIRE = os.environ.get('ACCESS_TOKEN_EXPIRE')

#Data Base
DATABASE = os.environ.get('DATABASE')
SCHEMA = os.environ.get('SCHEMA')
USER = os.environ.get('DB_USER')
PORT = os.environ.get('PORT')
HOST = os.environ.get('HOST')
PASSWORD = os.environ.get('PASSWORD')