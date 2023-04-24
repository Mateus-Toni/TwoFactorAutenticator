from fastapi import APIRouter, Depends, HTTPException, status
from jose import jwt, JWTError
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

import utils
from dao.user_dao import UserDb
from parameters import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE

router = APIRouter()

@router.post('/login')
def login(user: OAuth2PasswordRequestForm = Depends()):

    data_db = UserDb.get_id_and_password_by_email(user)# usuário cadastrado??

    if data_db: # sim

        if utils.check_pwd_hash(password_hash=data_db['password_user'], password=user.password): # senha igual db

            token_data = UserDb.verify_if_user_have_token(data_db['id_user'])

            if token_data:

                is_revoked = UserDb.verify_if_token_is_revoked(token_data['id_token'])

                if is_revoked:

                    #atualiza data de expiraçao token banco
                    # apaga token do revoked

                    ...
                
                else:

                    ...


            else:

                ...
                

        else:

            raise HTTPException(detail={'msg': 'invalid data'},
                            status_code=status.HTTP_401_UNAUTHORIZED)

    else:

        raise HTTPException(detail={'msg': 'invalid data'},
                            status_code=status.HTTP_401_UNAUTHORIZED)