from flask import Flask
from flask_bcrypt import Bcrypt
from database.db import initialize_db
from resources.routes import initialize_routes
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
bcrypt = Bcrypt(app)
app.config['DATABASE'] = "DB.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/DB.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = []
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['UPLOAD_FOLDER'] = 'database/upload_posters'

db_session = initialize_db(app=app)
initialize_routes(api)


app.run()