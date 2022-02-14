from flask import Blueprint, request, jsonify

from flask import Response, request, make_response
from database.models import Film, User
from datetime import datetime
from database.db import db_session
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

class MoviesApi(Resource):
    def get(self):
        movies = Film.query.all()
        movies = list(map(lambda x: x.to_json(),movies))
        print(movies)
        return make_response(jsonify(movies), 200)

    @jwt_required()
    def post(self):
        print("1")
        user_id = get_jwt_identity()
        print("2")
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

class MovieApi(Resource):
    @jwt_required()
    def put(self, id):
        print(id)
        body = request.get_json()
        film = Film.query.get(id)
        film.title = body['title'] if 'title' in body else film.title
        film.date =  datetime.strptime(body['date'],'%d.%m.%Y') if 'date' in body else film.date
        db_session.commit()
        db_session.flush()
        return "", 200
    @jwt_required()
    def delete(self, id):

        body = request.get_json()
        film = Film.query.get(id)
        db_session.delete(film)
        db_session.commit()
        db_session.flush()
        return "", 200


    def get(self, id):
        film = Film.query.get(id)
        return make_response(film.to_json(), 200)


