from turtle import title
from flask import Flask
from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Film
from datetime import datetime

app = Flask(__name__)
app.config['DATABASE'] = "DB.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/DB.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = []
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['UPLOAD_FOLDER'] = 'database/upload_posters'
db_session = initialize_db(app=app)

@app.route('/movies')
def get_movies():
    movies = Film.query.all()
    movies = list(map(lambda x: x.to_json(),movies))
    return jsonify(movies)


@app.route('/movies', methods=['POST'])
def add_movies(): 
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

@app.route('/movies/<int:index>', methods=['PUT'])
def update_movie(index): 
    body = request.get_json()
    film = Film.query.get(index)
    film.title = body['title'] if 'title' in body else film.title
    film.date =  datetime.strptime(body['date'],'%d.%m.%Y') if 'date' in body else film.date
    db_session.commit()
    db_session.flush()
    return "", 200

@app.route('/movies/<int:index>', methods=['DELETE'])
def delete_movie(index): 
    body = request.get_json()
    film = Film.query.get(index)
    db_session.delete(film)
    db_session.commit()
    db_session.flush()
    return "", 200


app.run()