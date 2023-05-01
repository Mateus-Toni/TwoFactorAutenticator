from pydantic import BaseModel, Field

class User(BaseModel):

    name_user: str
    last_name: str
    birth_day: str
    cpf: str
    password_user: str
    email: str
    nick_name: str


class Code(BaseModel):

    code: str#colocar regex

