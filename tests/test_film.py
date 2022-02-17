
from http.client import responses
import unittest
import json
from urllib import response

from app import app
from database.db import db
from database.models import Film, User
from datetime import datetime

EMAIL = "test@mail.ru"
PASS = "111222"
DATE = "18.02.1997"
class FilmTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()
            user = User(EMAIL, PASS)
            user.save()
            db.session.flush()
            film = Film()
            film.title = "Name_title"
            film.date = datetime.strptime(DATE, '%d.%m.%Y')
            film.user_id = user.id
            film.save()

    def test_successful_get_films(self):
        # When
        with app.app_context():
            response = self.app.get(
                '/api/films'
            )

        self.assertEqual(list, type(response.json['movies']))
        self.assertEqual(200, response.status_code)

    def test_successful_post_films(self):
        with app.app_context():
            response = self.add_film()
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)

    def test_successful_put_film(self):
        token = self.login()
        film_id = self.add_film().json['id']
        payload = json.dumps({
            'title': 'Changed Title'
        })
        with app.app_context():
            response = self.app.put(
                f'/api/films/{film_id}',
                headers={"Content-Type": "application/json",
                        "Authorization": token},
                data=payload
            )
        self.assertEqual(200, response.status_code)
        
    def test_successful_delete_film(self):
        token = self.login()
        film_id = self.add_film().json['id']
        with app.app_context():
            response = self.app.delete(
                f'/api/films/{film_id}',
                headers={"Content-Type": "application/json",
                        "Authorization": token},
            )
        self.assertEqual(200, response.status_code)

    def login(self):
        payload = json.dumps({
            "email": EMAIL,
            "password": PASS
        })

        # When
        with app.app_context():
            token = self.app.post(
                '/api/auth/login',
                headers={"Content-Type": "application/json"},
                data=payload
            ).json['token']
        return f"Bearer {token}"

    def add_film(self):
        token = self.login()
        payload_film = {
            "title": "Title 2",
            "date": "18.02.1999"
        }

        response = self.app.post(
            '/api/films',
            headers={"Content-Type": "application/json",
                     "Authorization": token},
            data=json.dumps(payload_film)
        )
        return response

    def tearDown(self):
        with app.app_context():

            db.session.remove()
            db.drop_all()
