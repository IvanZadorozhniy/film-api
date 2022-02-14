from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()
db_session = db.session

def initialize_db(app):
    db.init_app(app)
    migrate = Migrate(app, db)
    db.create_all(app=app)
    return db.session
    