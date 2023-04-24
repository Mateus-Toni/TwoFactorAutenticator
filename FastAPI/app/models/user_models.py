from pydantic import BaseModel

class User(BaseModel):

    name_user: str
    last_name: str
    birth_day: str
    cpf: str
    password_user: str
    email: str
    nick_name: str

