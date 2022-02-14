from .db import db
from flask_bcrypt import generate_password_hash, check_password_hash
# FilmGenre = db.Table('FilmGenre', db.Model.metadata,
#                      db.Column('film_id', db.ForeignKey('film.id')),
#                      db.Column('genre_id', db.ForeignKey('genre.id'))
#                      )
# FilmDirector = db.Table('FilmDirector', db.Model.metadata,
#                         db.Column('film_id', db.ForeignKey('film.id')),
#                         db.Column('director_id', db.ForeignKey('director.id'))
#                         )


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    films = db.relationship("Film", backref='user')
#     api_key = db.Column(db.String)

    def __init__(self, email, password) -> None:
        super().__init__()
        # self.username = username
        self.password = password
        self.email = email

#     def __repr__(self):
#         return '{} {} {} {}'.format(self.id, self.username, self.email, self.api_key)
    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Film(db.Model):
    __tablename__ = 'film'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def to_json(self):
        json_student = {
            'id': str(self.id),
            'title': str(self.title),
            'date': str(self.date),
            'user_id': str(self.user_id)
        }

        return json_student

    # describe = db.Column(db.Text)
    # rating = db.Column(db.Float)
    # poster_path = db.Column(db.String)
        # genre = db.relationship('Genre', secondary=FilmGenre)


# class Genre(db.Model):
#     __tablename__ = 'genre'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, unique=True, nullable=False)


# class Director(db.Model):
#     __tablename__ = 'director'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String)
#     last_name = db.Column(db.String)
