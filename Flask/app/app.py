from flask import Flask, request
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from werkzeug.security import check_password_hash

import parameters
from users.User_model import User

app = Flask(__name__)
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = parameters.ACCESS_EXPIRES
app.config["JWT_SECRET_KEY"] = parameters.SECRET_KEY
app.debug = True

@app.route('/')
def healthy():

    return {'msg': 'im alive'}


@app.route('/login')
def login():

    pass

@app.route('/register', methods=['POST'])
def register():

    try:

        data_user = request.get_json()

    except Exception as r:

        return {'msg': 'missing json data'}

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