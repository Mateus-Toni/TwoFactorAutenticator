from flask import Flask
from flask_jwt_extended import create_access_token, jwt_required, JWTManager
from werkzeug.security import check_password_hash

import parameters

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


if __name__ == '__main__':

    app.run(port=parameters.APP_PORT)