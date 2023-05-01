from datetime import datetime, timedelta
from random import randint
import logging

from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer

import utils
from models.user_models import Code
from dao.user_dao import UserDb
from parameters import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE

router = APIRouter()

oauth = OAuth2PasswordBearer(tokenUrl="login")

def two_auth_journey(id_user: int, email: str):

    code = randint(10000, 999999)
    UserDb.save_code_in_db(code=code, id_user=id_user)
    logging.info(code) #envia código no email

    payload = {
        'user_id': id_user,
        'sub': email,
        'exp': datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE),
        'type': 'code',
        'two_auth': False
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    return token

def verify_token(token: str = Depends(oauth)):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        user_email = payload['sub']
        data_db = UserDb.get_id_and_password_by_email(user_email)
        token_data = UserDb.verify_if_user_have_token(data_db['id_user'])

        if not data_db and token_data:

            raise HTTPException(detail={'msg': 'invalid token'}, 
                             status_code=status.HTTP_401_UNAUTHORIZED)
        
        if UserDb.verify_if_token_is_revoked(data_db['id_user'], token):

            raise HTTPException(detail={'msg': 'invalid token'}, 
                             status_code=status.HTTP_401_UNAUTHORIZED)
        
        #add ip 

    except JWTError:

        raise HTTPException(detail={'msg': 'missing token'}, 
                             status_code=status.HTTP_401_UNAUTHORIZED)
    


@router.post('/login')
def login(user: OAuth2PasswordRequestForm = Depends()):

    data_db = UserDb.get_id_and_password_by_email(user)# usuário cadastrado??

    if data_db:

        if utils.check_pwd_hash(password_hash=data_db['password_user'], password=user.password): # senha igual db

            token_data = UserDb.verify_if_user_have_token(data_db['id_user'])

            if token_data:

                date_now = datetime.now().date()

                date_last_two_auth = token_data['date_two_auth']

                if (date_now - date_last_two_auth).days <= 10:

                    payload = {
                        'user_id': data_db['id_user'],
                        'sub': user.username,
                        'exp': datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE),
                        'type': 'two_auth',
                        'two_auth': True
                    }

                    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

                    if UserDb.update_last_two_auth(id_two_auth=token_data['id_two_auth']):

                        return JSONResponse(
                            content={'access_token': token, "type": 'two_auth'},
                            status_code=status.HTTP_200_OK
                        )
                    
                    raise HTTPException(detail={'msg': 'error db'},
                            status_code=status.HTTP_401_UNAUTHORIZED)

                else: 

                    access_token = two_auth_journey(data_db['id_user'], user.username)
                    
                    return JSONResponse(
                        content={'access_token': access_token, 'type': 'code'},
                        status_code=status.HTTP_200_OK
                    )
                
            else:

                access_token = two_auth_journey(data_db['id_user'], user.username)
                
                return JSONResponse(
                    content={'access_token': access_token, 'type': 'code'},
                    status_code=status.HTTP_200_OK
                )
                
        else:

            raise HTTPException(detail={'msg': 'invalid data'},
                            status_code=status.HTTP_401_UNAUTHORIZED)

    else:

        raise HTTPException(detail={'msg': 'invalid data'},
                            status_code=status.HTTP_401_UNAUTHORIZED)

@router.post('/two_auth')
def two_auth(code: Code, token: str = Depends(verify_token)):
    ...
