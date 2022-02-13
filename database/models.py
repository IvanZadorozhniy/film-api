from .db import db

# FilmGenre = db.Table('FilmGenre', db.Model.metadata,
#                      db.Column('film_id', db.ForeignKey('film.id')),
#                      db.Column('genre_id', db.ForeignKey('genre.id'))
#                      )
# FilmDirector = db.Table('FilmDirector', db.Model.metadata,
#                         db.Column('film_id', db.ForeignKey('film.id')),
#                         db.Column('director_id', db.ForeignKey('director.id'))
#                         )


# class User(db.Model):
#     __tablename__ = 'user'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String, unique=True, nullable=False)
#     email = db.Column(db.String, unique=True, nullable=False)
#     password = db.Column(db.String, nullable=False)
#     films = db.relationship("Film", backref='user')
#     api_key = db.Column(db.String)

#     def __init__(self, username, email, password) -> None:
#         super().__init__()
#         self.username = username
#         self.password = password
#         self.email = email

#     def __repr__(self):
#         return '{} {} {} {}'.format(self.id, self.username, self.email, self.api_key)


class Film(db.Model):
    __tablename__ = 'film'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.Date)
    def to_json(self):
        json_student = {
            'id': self.id,
            'title': self.title,
            'date': self.date,
        }

        return json_student
    # describe = db.Column(db.Text)
    # rating = db.Column(db.Float)
    # poster_path = db.Column(db.String)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
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



