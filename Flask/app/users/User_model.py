
from werkzeug.security import generate_password_hash

from dao.user_dao import UserDb
import users.utils as utils

class User:

    def __init__(self, name_user, last_name, birth_day, cpf, password_user, email, nick_name):

        self._id_user = None
        self.name_user = name_user
        self.last_name = last_name
        self.birth_day = birth_day
        self.cpf = cpf
        self.password_user = generate_password_hash(password_user) 
        self.email  = email 
        self.nick_name = nick_name


    def set_id(self, id_db: int):

        self._id_user = id_db


    def create_user(self):

        already_exists = UserDb.verify_if_user_exists(self)

        if already_exists:

            return 'user already exist', 401

        else:

            is_valid = utils.validate_data_user(self)

            if is_valid:

                is_cpf = utils.cpf_autenticator(self.cpf)

                if is_cpf:

                    success = UserDb.create_user_in_db(self)

                    if success:

                        return 'user created', 200

                    else:

                        return 'error in database', 401

                else:

                    return 'invalid cpf', 401

            else:

                return 'invalid data user', 401

