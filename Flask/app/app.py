from random import randint
from datetime import timedelta, datetime

from flask import Flask, request
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager
from flask_jwt_extended import get_jwt
from flask_jwt_extended import get_jwt_identity
from werkzeug.security import check_password_hash

import parameters
from users.utils import send_email
from users.User_model import User
from dao.user_dao import UserDb

app = Flask(__name__)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = parameters.ACCESS_EXPIRES
app.config["JWT_SECRET_KEY"] = parameters.SECRET_KEY
app.debug = True
jwt = JWTManager(app)

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

            if token_data and check_password_hash(password=password, pwhash=password_db):

                if not UserDb.verify_if_token_is_revoked(token_data['id_token']):

                    jwt = token_data['user_token']

                    create_date = token_data['create_date']

                    date_now = datetime.now().date()
                    
                    if (date_now - create_date).days <= 3 and token_data['flag'] == 'two_auth':

                        return {'msg': jwt}, 200

                    elif token_data['flag'] == 'recover_password':

                        return {'msg': 'recover password token: invalid token for login'}, 400

                    elif token_data['flag'] == 'code':

                        return {'msg': 'token for two auth: invalid token for login'}, 400

                    elif (date_now - create_date).days > 3 and token_data['flag'] == 'two_auth':

                        #adicionar token ao revogado
                        UserDb.delete_jwt_by_id(id_user=id_user)
                        UserDb.delete_code_by_id(id_user=id_user)
                        
                        code = randint(100000, 999999)

                        saved = UserDb.save_code_in_db(code=code, id_user=id_user)

                        access_token = create_access_token(identity=id_user, additional_claims={'two_auth': False, 'type': 'code'}, expires_delta=timedelta(days=1))

                        token_success = UserDb.save_token_in_db(id_user=id_user, user_token=access_token, flag='code')

                        if saved and token_success:

                            #send_email(email, parameters.CODE_LAYOUT.format(code=code))

                            return {'msg': access_token}, 200

                        else:

                            return {'msg': 'error in db'}, 400

                else:

                    UserDb.delete_jwt_by_id(id_user=id_user) #trocar para revogar token
                    UserDb.delete_code_by_id(id_user=id_user)
                    
                    code = randint(100000, 999999)

                    saved = UserDb.save_code_in_db(code=code, id_user=id_user)

                    access_token = create_access_token(identity=id_user, additional_claims={'two_auth': False, 'type': 'code'}, expires_delta=timedelta(days=1))

                    token_success = UserDb.save_token_in_db(id_user=id_user, user_token=access_token, flag='code')

                    if saved and token_success:

                        #send_email(email, parameters.CODE_LAYOUT.format(code=code))

                        return {'msg': access_token}, 200

                    else:

                        return {'msg': 'error in db'}, 400
            
            elif check_password_hash(password=password, pwhash=password_db):

                code = randint(100000, 999999)

                saved = UserDb.save_code_in_db(code=code, id_user=id_user)

                access_token = create_access_token(identity=id_user, additional_claims={'two_auth': False, 'type': 'code'}, expires_delta=timedelta(days=1))

                token_success = UserDb.save_token_in_db(id_user=id_user, user_token=access_token, flag='code')

                if saved and token_success:

                    #send_email(email, parameters.CODE_LAYOUT.format(code=code))

                    return {'msg': access_token}, 200

                else:

                    return {'msg': 'error in db'}, 400

            else:

                return {'msg': 'wrong input'}, 400

        else:

            return {'msg': 'wrong input'}, 400


@app.route('/code', methods=['POST'])
@jwt_required()
def two_auth():
    
    id_user = get_jwt_identity()
    jwt = get_jwt()

    if (not jwt['two_auth']) and jwt['type'] == 'code':

        try:

            code = request.get_json()

        except Exception as r:

            return {'msg': 'missing json data'}, 400

        else:

            data_code = UserDb.get_code_by_id(id_user)

            if str(code) == str(data_code['code']):
                
                if data_code['create_date'] <= data_code['create_date'] + timedelta(days=1):
                    
                    jti = get_jwt()['jti']

                    revoked_old_token = UserDb.revoked_token(id_user=id_user, jti=jti)

                    if revoked_old_token:

                        DataBaseTwoAuth.delete_jwt_by_id_user(id_user)

                        new_access_token = create_access_token(
                            identity=id_user,
                            expires_delta=timedelta(days=3),
                            additional_claims={'two_auth': True, 'type': 'autorization'}
                            )

                        DataBaseTwoAuth.create_jwt(id_user=id_user, jwt=new_access_token)

                        return {'access_token': new_access_token}, 200

                else:

                    return {'msg': 'invalid code'}, 400

            else:

                return {'msg': 'wrong code'}, 400

    elif jwt['type'] == 'autorization' and jwt['two_auth']:

        return {'msg': 'user have two_auth'}, 200

    elif (not jwt['two_auth']) and jwt['type'] == 'password_recover':

        ...


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