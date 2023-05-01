import logging
from datetime import datetime

from psycopg2 import sql

import utils
from dao.db import DataBase
from models.user_models import User
from parameters import HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA

class UserDb:

    @staticmethod
    def create_user_in_db(user: User) -> bool:
        """
        _summary_

        Args:
            user (object): _description_

        Returns:
            bool: _description_
        """

        pwd_hash = utils.get_pwd_hash(user.password_user)

        query = sql.SQL(
            '''
            insert into users 
            (name_user, last_name, birth_day, cpf, password_user, email, nick_name)
            values
            ({name_user}, {last_name}, {birth_day}, {cpf}, {password_user}, {email}, {nick_name})
            ;
            ''' 
        ).format(
            name_user=sql.Literal(user.name_user),
            last_name=sql.Literal(user.last_name),
            birth_day=sql.Literal(user.birth_day),
            cpf=sql.Literal(user.cpf),
            password_user=sql.Literal(pwd_hash),
            email=sql.Literal(user.email),
            nick_name=sql.Literal(user.nick_name)
        )

        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:
                
                logging.critical(r)
                return False

            else:

                return True


    @staticmethod
    def delete_user_by_cpf(user: object) -> bool:
        """
        _summary_

        Args:
            user (object): _description_

        Returns:
            bool: _description_
        """

        query = sql.SQL(
            '''
            delete from users
            where
            cpf = {cpf}
            ;
            '''
        ).format(
            cpf=sql.Literal(user.cpf)
        )

        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical('-'*20)
                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> delete_user_by_cpf')
                logging.critical('-'*20)
                
                return False

            else:

                return True


    @staticmethod
    def update_user(user: object) -> bool:
        """
        _summary_

        Args:
            user (object): _description_

        Returns:
            bool: _description_
        """

        query = sql.SQL(
            '''
            update users 
            set 
            name_user = {name_user},
            last_name = {last_name},
            birth_day = {birth_day},
            email = {email},
            nick_name = {nick_name}  
            where 
            id_user = {id_user}
            ;
            '''
        ).format(
            name_user=sql.Literal(user.name_user),
            last_name=sql.Literal(user.last_name),
            birth_day=sql.Literal(user.birth_day),
            email=sql.Literal(user.email),
            nick_name=sql.Literal(user.nick_name),
            id_user=sql.Literal(user.id_user)
        )
        
        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical('-'*20)
                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> update_user')
                logging.critical('-'*20)
                
                return False

            else:

                return True


    @staticmethod
    def get_user_id_by_cpf(user: object) -> int:
        """
        _summary_

        Args:
            user (object): _description_

        Returns:
            int: _description_
        """

        query = sql.SQL(
            '''
            select id_user from users
            where 
            cpf = {cpf}
            ;
            '''
        ).format(
            cpf=sql.Literal(user.cpf)
        )

        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical('-'*20)
                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> get_user_id_by_cpf')
                logging.critical('-'*20)
                
                return False

            else:

                return cursor.fetchall()['id_user']


    @staticmethod
    def verify_if_user_exists(user: User) -> bool:
        """
        _summary_

        Args:
            user (object): _description_

        Returns:
            bool: _description_
        """

        query = sql.SQL(
            '''
            select * from users
            where 
            cpf = {cpf}
            ;
            '''
        ).format(
            cpf=sql.Literal(user.cpf)
        )

        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:
            

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical(r)
                return False

            else:  

                return not bool(cursor.fetchall())

    
    @staticmethod
    def get_id_and_password_by_email(user: User) -> dict:
        """
        _summary_

        Args:
            email (str): _description_

        Returns:
            dict: _description_
        """

        query = sql.SQL(
            '''
            select id_user, password_user from users
            where 
            email = {email}
            ;
            '''
        ).format(
            email=sql.Literal(user.username)
        )

        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> get_password_by_email')
            
                return False

            else:

                return cursor.fetchone()

    
    @staticmethod
    def verify_if_user_have_token(id_user: int) -> dict:

        query = sql.SQL(
            '''
            select id_two_auth, two_auth, date_two_auth from two_auth
            where
            id_user = {id_user}
            ;
            '''
        ).format(
            id_user=sql.Literal(id_user)
        )

        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> verify_if_user_have_token')
            
                return False

            else:

                return cursor.fetchone()

    
    @staticmethod
    def save_code_in_db(code: int, id_user: int) -> bool:
        """
        _summary_

        Args:
            code (int): _description_
            id_user (int): _description_

        Returns:
            bool: _description_
        """

        query = sql.SQL(
            '''
            insert into two_auth 
            (id_user, user_code, two_auth) 
            values 
            ({id_user}, {user_code}, {two_auth})
            ;
            '''
        ).format(
            id_user=sql.Literal(id_user),
            user_code=sql.Literal(code),
            two_auth=sql.Literal('false'),
        )
        
        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical('-'*20)
                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> save_code_in_db')
                logging.critical('-'*20)
                
                return False

            else:

                return True

    
    @staticmethod
    def delete_code_by_id(id_user):

        query = sql.SQL(
            '''
            delete from code_user 
            where 
            id_user = {id_user}
            ;
            '''
        ).format(
            id_user=sql.Literal(id_user),
        )
        
        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical('-'*20)
                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> delete_code_by_id')
                logging.critical('-'*20)
                
                return False

            else:

                return True

    
    @staticmethod
    def get_code_by_id(id_user):

        query = sql.SQL(
            '''
            select user_code, create_date from code_user 
            where 
            id_user = {id_user}
            ;
            '''
        ).format(
            id_user=sql.Literal(id_user),
        )
        
        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical('-'*20)
                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> delete_code_by_id')
                logging.critical('-'*20)
                
                return False

            else:

                return cursor.fetchall()


    @staticmethod
    def revoked_token(jti, id_user, id_token):

        query = sql.SQL(
            '''
            insert into revoked_token
            (id_token, id_user, user_jti)
            values
            ({id_token}, {id_user}, {user_jti})
            ;
            '''
        ).format(
            id_token=sql.Literal(id_token),
            id_user=sql.Literal(id_user),
            user_jti=sql.Literal(jti)
        )
        
        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical('-'*20)
                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> revoked_token')
                logging.critical('-'*20)
                
                return False

            else:

                return True


    @staticmethod
    def verify_if_token_is_revoked(id_user, token):
        """
        _summary_

        Args:
            id_token (_type_): _description_

        Returns:
            _type_: _description_
        """

        query = sql.SQL(
            '''
            select * from revoked_token
            where
            id_user = {id_user}
            and 
            user_token = {token}
            ;
            '''
        ).format(
            id_user=sql.Literal(id_user),
            token=sql.Literal(token)
        )
        
        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical('-'*20)
                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> revoked_token')
                logging.critical('-'*20)
                
                return True

            else:

                return bool(cursor.fetchall())
            

    def update_last_two_auth(id_two_auth):

        query = sql.SQL(
            '''
            update two_auth
            set two_auth = 'true', date_two_auth = {date}
            where id_two_auth = {id_two_auth};
            ;
            '''
        ).format(
            date=sql.Literal(datetime.now().date()),
            id_two_auth=sql.Literal(id_two_auth),
        )
        
        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.critical('-'*20)
                logging.critical(r)
                logging.critical('error in DataBase')
                logging.critical('app/dao/user_dao.py -> revoked_token')
                logging.critical('-'*20)
                
                return False

            else:

                return True
