from flask import Blueprint, request, jsonify

from flask import Response, request, make_response
from database.models import Film, User
from datetime import datetime
from database.db import db_session
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import exc
from resources.error import SchemaValidationError, MovieAlreadyExistsError, \
InternalServerError, UpdatingMovieError, DeletingMovieError, MovieNotExistsError

class MoviesApi(Resource):
    def get(self):
        movies = Film.query.all()
        movies = list(map(lambda x: x.to_json(),movies))
        print(movies)
        return make_response(jsonify(movies), 200)

    @jwt_required()
    def post(self):
        try:
            user_id = get_jwt_identity()
            user = User.query.get(user_id)
            body = request.get_json()
            title = body['title']
            date = body['date']
            film = Film()
            film.title = str(title)
            film.date = datetime.strptime(date, '%d.%m.%Y')
            film.user_id = user_id
            user.films.append(film)
            db_session.add(film)
            db_session.commit()
            db_session.flush()
            return {'id': str(film.id)}, 200
        except exc.IntegrityError as e:
            raise MovieAlreadyExistsError
        except exc.SQLAlchemyError as e:
            print(type(e))
        except Exception as e:
            raise InternalServerError

class MovieApi(Resource):
    @jwt_required()
    def put(self, id):
        try:
            body = request.get_json()
            film = Film.query.get(id)
            film.title = body['title'] if 'title' in body else film.title
            film.date =  datetime.strptime(body['date'],'%d.%m.%Y') if 'date' in body else film.date
            db_session.commit()
            db_session.flush()
            return "", 200
        except exc.InvalidRequestError as e:
             raise SchemaValidationError
        except exc.NoSuchTableError as e:
            raise UpdatingMovieError
        except exc.NoResultFound as e:
            raise UpdatingMovieError
        except Exception as e:
            raise InternalServerError 

    @jwt_required()
    def delete(self, id):
        try:
            body = request.get_json()
            film = Film.query.get(id)
            db_session.delete(film)
            db_session.commit()
            db_session.flush()
            return "", 200
        except exc.NoSuchTableError as e:
            raise DeletingMovieError
        except Exception as e:
            raise InternalServerError 


    def get(self, id):
        try:
            film = Film.query.get(id)
            return make_response(film.to_json(), 200)
        except exc.NoSuchTableError as e:
            raise MovieNotExistsError
        except Exception as e:
            raise InternalServerError 


