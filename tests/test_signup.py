
from re import S
import unittest
import json

from app import app
from database import db
from database.models import User
class SignupTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.db = db.db

    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "email": "paurakh011@gmail.com",
            "password": "mycoolpassword"
        })

        # When
        response = self.app.post('/api/auth/signup', headers={"Content-Type": "application/json"}, data=payload)

        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)

    def tearDown(self):
        with app.app_context():
        
            self.db.session.remove()
            self.db.drop_all()