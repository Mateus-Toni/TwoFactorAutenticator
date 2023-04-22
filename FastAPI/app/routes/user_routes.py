from fastapi import APIRouter

from models import user_models

router =  APIRouter()

@router.post('/register')
def register_user():

    return 'register'

@router.post('/update')
def update_user():

    return 'update'

@router.post('/delete/{id_user}')
def delete_user(id_user: int):

    return f'delete user : {id_user}'

@router.post('/get_user/')
def get_user(q: str):

    return f'user {q}'