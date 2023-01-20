import logging

import psycopg2

class DataBase:
    
    def __init__(self, hostname, username, port, password, db, schema):

        self.hostname = hostname 
        self.username = username 
        self.port = port 
        self.password = password
        self.db = db
        self.schema = schema

    def __enter__(self):

        try:

            self.db = psycopg2.connect(
                host=self.hostname,
                user=self.username,
                password=self.password,
                port=self.port,
                dbname=self.db
            )
            self.cursor = self.db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            self.cursor.execute(f"set schema '{self.schema}'")

        except Exception as erro:
            
            logging.error(f"Error database can't connect: {erro}")
            self.db.close()

        else:

            return self.cursor

    def __exit__(self, *args):

        try:

            self.db.commit()
            self.db.close()

        except Exception as erro:

            logging.error(f'Database error: {erro}')
            self.db.close()

        else:

            return self.cursor


