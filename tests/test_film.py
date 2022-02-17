
import unittest
import json
from urllib import response

from app import app
from database.db import db
from database.models import Film, User
from datetime import datetime
class FilmTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()
            user = User("test@mail.ru", "111222")
            user.save()
            db.session.flush()
            film = Film()
            film.title = "Name_title"
            film.date = datetime.strptime("18.02.1997", '%d.%m.%Y')
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
    
        
    def tearDown(self):
        with app.app_context():

            db.session.remove()
            db.drop_all()
