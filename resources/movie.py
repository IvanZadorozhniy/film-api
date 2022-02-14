from flask import Blueprint, request, jsonify

from flask import Response, request
from database.models import Film
from datetime import datetime
from database.db import db_session
from flask_restful import Resource

class MoviesApi(Resource):
  def get(self):
    movies = Film.query.all()
    movies = list(map(lambda x: x.to_json(),movies))
    return Response(jsonify(movies), mimetype="application/json", status=200)

  def post(self):
    body = request.get_json()
    title = body['title']
    date = body['date']
    film = Film()
    film.title = str(title)
    film.date = datetime.strptime(date, '%d.%m.%Y')
    db_session.add(film)
    db_session.commit()
    db_session.flush()
    return {'id': str(film.id)}, 200   

class MovieApi(Resource):
    def put(self, id):
        body = request.get_json()
        film = Film.query.get(id)
        film.title = body['title'] if 'title' in body else film.title
        film.date =  datetime.strptime(body['date'],'%d.%m.%Y') if 'date' in body else film.date
        db_session.commit()
        db_session.flush()
        return "", 200
    def delete(self, id):
        body = request.get_json()
        film = Film.query.get(id)
        db_session.delete(film)
        db_session.commit()
        db_session.flush()
        return "", 200


    def get(self, id):
        film = Film.query.get(id)
        return Response(film, mimetype="application/json", status=200)


