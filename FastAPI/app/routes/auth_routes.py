from fastapi import APIRouter
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext

from parameters import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE

router = APIRouter()

@router.post('/login')
def login():

    return 'login'