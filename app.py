from flask import Flask
from flask_bcrypt import Bcrypt
from database.db import initialize_db

from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_mail import Mail

from resources.error import errors


app = Flask(__name__)
app.config.from_envvar('ENV_FILE_LOCATION')
app.config['DATABASE'] = "DB.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/DB.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = []
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['UPLOAD_FOLDER'] = 'database/upload_posters'
api = Api(app, errors=errors)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
mail = Mail(app)
from resources.routes import initialize_routes

db_session = initialize_db(app=app)
initialize_routes(api)

