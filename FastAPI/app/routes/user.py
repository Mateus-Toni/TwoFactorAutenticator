from fastapi import APIRouter, status, HTTPException
from fastapi.responses import JSONResponse

from models.user_models import User
from dao.user_dao import UserDb

router =  APIRouter()

@router.post('/register')
def register_user(user: User):

    # verificar infos usuario

    exist = UserDb.verify_if_user_exists(user)

    if exist:
        
        sucess = UserDb.create_user_in_db(user)

        if sucess:

            return JSONResponse(content={'msg': 'user create'},
                                status_code=status.HTTP_201_CREATED)
        
        else:

            return HTTPException(detail={'msg': 'error in db'},
                            status_code=status.HTTP_401_UNAUTHORIZED)

    else:

        raise HTTPException(detail={'msg': 'User already exists'},
                            status_code=status.HTTP_401_UNAUTHORIZED)

