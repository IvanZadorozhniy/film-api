import datetime

from database.db import db_session
from database.models import User
from flask import render_template, request
from flask_jwt_extended import create_access_token, decode_token
from flask_restful import Resource
from services.mail_service import send_email

from resources.error import (EmailDoesnotExistsError,
                             SchemaValidationError)


class ForgotPassword(Resource):
    """ForgotPassword Forgot password .

    Args:
        Resource ([type]): [description]
    """
    def post(self):
        url = request.host_url + 'api/auth/reset/'
        body = request.get_json()
        email = body.get('email')
        if not email:
            raise SchemaValidationError

        user = User.get_by_email(email)
        if not user:
            raise EmailDoesnotExistsError

        expires = datetime.timedelta(hours=24)
        reset_token = create_access_token(str(user.id), expires_delta=expires)

        return send_email('[Movie-bag] Reset Your Password',
                          sender='support@movie-bag.com',
                          recipients=[user.email],
                          text_body=render_template('email/reset_password.txt',
                                                    url=url + reset_token),
                          html_body=render_template('email/reset_password.html',
                                                    url=url + reset_token))


class ResetPassword(Resource):
    """ResetPassword Reset the password .

    Args:
        Resource ([type]): [description]
    """
    def post(self):

        body = request.get_json()
        reset_token = body.get('reset_token')
        password = body.get('password')

        if not reset_token or not password:
            raise SchemaValidationError

        user_id = decode_token(reset_token)['sub']
        user = User.get_by_id(user_id)

        user.password = password
        user.hash_password()
        db_session.commit()
        db_session.flush()

        return send_email('[Movie-bag] Password reset successful',
                          sender='support@movie-bag.com',
                          recipients=[user.email],
                          text_body='Password reset was successful',
                          html_body='<p>Password reset was successful</p>')
