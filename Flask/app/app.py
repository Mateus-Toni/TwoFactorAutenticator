from random import randint
from datetime import timedelta, datetime

from flask import Flask, request
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from werkzeug.security import check_password_hash

import parameters
from users.utils import send_email
from users.User_model import User
from dao.user_dao import UserDb

app = Flask(__name__)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = parameters.ACCESS_EXPIRES
app.config["JWT_SECRET_KEY"] = parameters.SECRET_KEY
app.debug = True

@app.route('/')
def healthy():

    return {'msg': 'im alive'}


@app.route('/login', methods=['POST'])
def login():

    try:

        data_user = request.get_json()

    except Exception as r:

        return {'msg': 'missing json data'}, 400

    else:

        email = data_user['email']
        password = data_user['password']

        data_db = UserDb.get_id_and_password_by_email(email)

        if data_db:

            id_user = data_db['id_user']
            password_db = data_db['password_user'] 

            token_data = UserDb.verify_if_user_have_token(id_user)

            if token_data:

                jwt = token_data['user_token']

                create_data = token_data['create_data']

                date_now = datetime.now()
                
                if (date_now - create_data).days <= 3:

                    if jwt['two_auth']:

                        return {'msg': jwt}, 200

                    else:

                        return {'msg': 'two auth is false'}, 400

                else:

                    UserDb.delete_jwt_by_id(id_user=id_user)
                    UserDb.delete_code_by_id(id_user=id_user)
                    
                    code = randint(100000, 999999)

                    saved = UserDb.save_code_in_db(code=code, id_user=id_user)

                    access_token = create_access_token(identity=id_user, additional_claims={'two_auth': False}, expires_delta=timedelta(days=1))

                    token_success = UserDb.save_token_in_db(id_user=id_user, user_token=access_token)

                    if saved and token_success:

                        send_email(email, parameters.CODE_LAYOUT.format(code=code))

                        return {'msg': access_token}, 200

                    else:

                        return {'msg': 'error in db'}, 400
            
            else:

                if check_password_hash(password=password, pwhash=password_db):

                    UserDb.delete_jwt_by_id(id_user=id_user)
                    UserDb.delete_code_by_id(id_user=id_user)

                    code = randint(100000, 999999)

                    saved = UserDb.save_code_in_db(code=code, id_user=id_user)

                    access_token = create_access_token(identity=id_user, additional_claims={'two_auth': False}, expires_delta=timedelta(days=1))

                    token_success = UserDb.save_token_in_db(id_user=id_user, user_token=access_token)

                    if saved and token_success:

                        send_email(email, parameters.CODE_LAYOUT.format(code=code))

                        return {'msg': access_token}, 200

                    else:

                        return {'msg': 'error in db'}, 400

                else:

                    return {'msg': 'wrong input'}, 400

        else:

            return {'msg': 'wrong input'}, 400




@app.route('/register', methods=['POST'])
def register():

    try:

        data_user = request.get_json()

    except Exception as r:

        return {'msg': 'missing json data'}, 400

    else:

        user = User(
            name_user = data_user['name_user'],
            last_name = data_user['last_name'],
            birth_day = data_user['birth_day'],
            cpf = data_user['cpf'],
            password_user = data_user['password_user'],
            email = data_user['email'],
            nick_name = data_user['nick_name']
        )
        
        msg, status_code = user.create_user()
        

        return {'msg': msg}, status_code


if __name__ == '__main__':

    app.run(port=parameters.APP_PORT)