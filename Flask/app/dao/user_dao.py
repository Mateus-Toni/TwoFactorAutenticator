import logging

from psycopg2 import sql

from dao import DataBase
from parameters import HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA

class UserDb:

    @staticmethod
    def create_user_in_db(user: object) -> bool:
        """
        _summary_

        Args:
            user (object): _description_

        Returns:
            bool: _description_
        """

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
            password_user=sql.Literal(user.password_user),
            email=sql.Literal(user.email),
            nick_name=sql.Literal(user.nick_name)
        )

        with DataBase(HOST, USER, PORT, PASSWORD, DATABASE, SCHEMA) as cursor:

            try: 
                
                cursor.execute(query)

            except Exception as r:

                logging.CRITICAL('-'*20)
                logging.CRITICAL(r)
                logging.CRITICAL('error in DataBase')
                logging.CRITICAL('app/dao/user_dao.py -> create_user_in_db')
                logging.CRITICAL('-'*20)
                
                return None

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

                logging.CRITICAL('-'*20)
                logging.CRITICAL(r)
                logging.CRITICAL('error in DataBase')
                logging.CRITICAL('app/dao/user_dao.py -> delete_user_by_cpf')
                logging.CRITICAL('-'*20)
                
                return None

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

                logging.CRITICAL('-'*20)
                logging.CRITICAL(r)
                logging.CRITICAL('error in DataBase')
                logging.CRITICAL('app/dao/user_dao.py -> update_user')
                logging.CRITICAL('-'*20)
                
                return None

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

                logging.CRITICAL('-'*20)
                logging.CRITICAL(r)
                logging.CRITICAL('error in DataBase')
                logging.CRITICAL('app/dao/user_dao.py -> get_user_id_by_cpf')
                logging.CRITICAL('-'*20)
                
                return None

            else:

                return cursor.fetchall()['id_user']
