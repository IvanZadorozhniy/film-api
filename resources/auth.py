from flask import request
from database.models import User
from flask_restful import Resource
from database.db import db_session
from flask import Response, request
from flask_jwt_extended import create_access_token
import datetime


class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        user.hash_password()
        db_session.add(user)
        db_session.commit()
        db_session.flush()
        id_ = user.id
        return {'id': str(id_)}, 200


class LoginApi(Resource):
    def post(self):
        body = request.get_json()
        user = User.query.filter(User.email.like(body.get('email'))).first()
        authorized = user.check_password(body.get('password'))
        if not authorized:
            return {'error': 'Email or password invalid'}, 401

        expires = datetime.timedelta(days=7)
        access_token = create_access_token(
            identity=str(user.id), expires_delta=expires)
        return {'token': access_token}, 200
