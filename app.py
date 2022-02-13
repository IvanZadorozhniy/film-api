from flask import Flask
from flask import Flask, jsonify, request, Response
from database.db import initialize_db
from database.models import Film

app = Flask(__name__)
app.config['DATABASE'] = "DB.sqlite"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/DB.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_BINDS'] = []
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = 'you-will-never-guess'
app.config['UPLOAD_FOLDER'] = 'database/upload_posters'
initialize_db(app=app)

@app.route('/movies')
def get_movies():
    movies = Film.query.all()
    movies = list(map(lambda x: x.to_json(),movies))
    return jsonify(movies)

# app.route('/add_movies', methods=['POST'])
# def add_movies():
#     movie =request.get_json()
#     movie.append(movie)
#     return {id: len(movies)}, 200

# @app.route('/movies/<int:index>', methods=['PUT'])
# def update_movie(index):
#     movie = request.get_json()
#     movies[index] = movie
#     return jsonify(movies[index]), 200

# @app.route('/movies/<int:index>', methods=['DELETE'])
# def delete_movie(index):
#     movies.pop(index)
#     return 'None', 200


app.run()