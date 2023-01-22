from dao.user_dao import UserDb

import utils

class User:

    def __init__(self, name_user, last_name, birth_day, cpf, password_user, email, nick_name):

        self._id_user = None
        self._name_user = name_user
        self._last_name = last_name
        self._birth_day = birth_day
        self._cpf = cpf
        self._password_user = password_user
        self._email  = email 
        self._nick_name = nick_name


    def set_id(self, id_db: int):

        self._id_user = id_db


    def create_user(self):

        return UserDb.create_user_in_db(self)

