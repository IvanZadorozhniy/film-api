from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
def initialize_db(app):
    db.init_app(app)
    db.create_all(app=app)
    return db.session
    