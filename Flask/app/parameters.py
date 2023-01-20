import os

from dotenv import load_dotenv

load_dotenv()

#database
#---------------------
DATABASE = os.environ.get('DATABASE')
SCHEMA = os.environ.get('SCHEMA')
USER = os.environ.get('DB_USER')
PORT = os.environ.get('PORT')
HOST = os.environ.get('HOST')
PASSWORD = os.environ.get('PASSWORD')
#=====================

#app config
#---------------------
SECRET_KEY = os.environ.get('SECRET_KEY')
ACCESS_EXPIRES = os.environ.get('ACCESS_EXPIRES')
APP_PORT = os.environ.get('APP_PORT')
#=====================