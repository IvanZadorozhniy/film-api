
import unittest
import json

from app import app
from database.db import db


class SignupTest(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        with app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_successful_signup(self):
        # Given
        payload = json.dumps({
            "email": "paurakh011@gmail.com",
            "password": "mycoolpassword"
        })

        # When
        with app.app_context():
            response = self.app.post(
                '/api/auth/signup',
                headers={"Content-Type": "application/json"},
                data=payload
            )
        print("test1")
        # Then
        self.assertEqual(str, type(response.json['id']))
        self.assertEqual(200, response.status_code)

    def test_failed_signup(self):
        payload = json.dumps({
            "email": "paurakh011gmail.com",
            "password": "mycoolpassword"
        })

        # When
        with app.app_context():
            response = self.app.post(
                '/api/auth/signup',
                headers={"Content-Type": "application/json"},
                data=payload
            )
        print("test1")
        # Then
        self.assertEqual(str, type(response.json['error']))
        self.assertEqual(400, response.status_code)
        
    def tearDown(self):
        with app.app_context():

            db.session.remove()
            db.drop_all()
