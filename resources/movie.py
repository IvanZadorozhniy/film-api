from datetime import datetime

from database.db import db_session
from database.models import Film, User
from flask import jsonify, make_response, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource
from sqlalchemy import exc

from resources.error import (DeletingMovieError, InternalServerError,
                             MovieAlreadyExistsError, MovieNotExistsError,
                             SchemaValidationError, UpdatingMovieError)


class MoviesApi(Resource):
    def get(self):
        movies = Film.query.all()
        movies = list(map(lambda x: x.to_json(), movies))
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
        except exc.IntegrityError:
            raise MovieAlreadyExistsError
        except exc.SQLAlchemyError as e:
            print(type(e))
        except Exception:
            raise InternalServerError


class MovieApi(Resource):
    @jwt_required()
    def put(self, id):
        try:
            body = request.get_json()
            film = Film.query.get(id)
            film.title = body['title'] if 'title' in body else film.title
            film.date = datetime.strptime(
                body['date'], '%d.%m.%Y') if 'date' in body else film.date
            db_session.commit()
            db_session.flush()
            return "", 200
        except exc.InvalidRequestError:
            raise SchemaValidationError
        except exc.NoSuchTableError:
            raise UpdatingMovieError
        except exc.NoResultFound:
            raise UpdatingMovieError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def delete(self, id):
        try:
            film = Film.query.get(id)
            db_session.delete(film)
            db_session.commit()
            db_session.flush()
            return "", 200
        except exc.NoSuchTableError:
            raise DeletingMovieError
        except Exception:
            raise InternalServerError

    def get(self, id):
        try:
            film = Film.query.get(id)
            return make_response(film.to_json(), 200)
        except exc.NoSuchTableError:
            raise MovieNotExistsError
        except Exception:
            raise InternalServerError
