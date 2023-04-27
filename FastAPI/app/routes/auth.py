from datetime import datetime, timedelta
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

code = OAuth2PasswordBearer(tokenUrl="login")
oauth2 = OAuth2PasswordBearer(tokenUrl="two_auth")

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

                    access_token = utils.two_auth_journey(data_db['id_user'])
                    
                    return JSONResponse(
                        content={'access_token': access_token, 'type': 'code'},
                        status_code=status.HTTP_200_OK
                    )
                
            else:

                access_token = utils.two_auth_journey(data_db['id_user'])
                
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


async def verify_token_two_auth(token: str = Depends(code)):
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        type_jwt = payload.get("type")
        user = payload.get("user_id")

        if type_jwt != 'code':

            raise credentials_exception
    
    except JWTError:

        raise credentials_exception
    
    #verificar c user existe
    #verificar c token é revogado
    #gerar esse squema para token two auth

    if user:

        return user
    
    raise credentials_exception
    

@router.post('/two_auth')
def two_auth(code: Code, token: ):

