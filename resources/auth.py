from flask import request
from database.models import User
from flask_restful import Resource
from database.db import db_session

class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        db_session.add(user)
        db_session.commit()
        db_session.flush()
        id = user.id
        return {'id': str(id)}, 200