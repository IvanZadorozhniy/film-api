
import resource
import unittest
import json

from app import app
from database.db import db
from database.db import initialize_db
from database.models import User

USER_MAIL = "test@gmail.com"
USER_PASS = "111111"
class LoginTest(unittest.TestCase):

    def setUp(self):
        with app.app_context():
            db.session.close()
            db.drop_all()
            db.create_all()
            
            user = User(email=USER_MAIL, password=USER_PASS)
            user.hash_password()
            db.session.add(user)
            db.session.commit()
        self.app = app.test_client()
        
        

    def test_successful_login(self):
        
        # Given
        payload = json.dumps({
            "email": USER_MAIL,
            "password": USER_PASS
        })

        # When
        with app.app_context():
            response = self.app.post(
                '/api/auth/login',
                headers={"Content-Type": "application/json"},
                data=payload
            )
            
        # Then
        self.assertEqual(str, type(response.json['token']))
        self.assertEqual(200, response.status_code)
    
    def test_failed_login(self):
        payload = json.dumps({
            "email": USER_MAIL,
            "password": "anotherPass"
        })

        # When
        with app.app_context():
            response = self.app.post(
                '/api/auth/login',
                headers={"Content-Type": "application/json"},
                data=payload
            )
            
        # Then
        self.assertEqual(str, type(response.json['error']))
        self.assertEqual(401, response.status_code)

    def tearDown(self):
        with app.app_context():

            db.session.remove()
            db.drop_all()
