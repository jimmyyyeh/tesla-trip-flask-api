# -*- coding: utf-8 -*
"""
      ┏┓       ┏┓
    ┏━┛┻━━━━━━━┛┻━┓
    ┃      ☃      ┃
    ┃  ┳┛     ┗┳  ┃
    ┃      ┻      ┃
    ┗━┓         ┏━┛
      ┗┳        ┗━┓
       ┃          ┣┓
       ┃          ┏┛
       ┗┓┓┏━━━━┳┓┏┛
        ┃┫┫    ┃┫┫
        ┗┻┛    ┗┻┛
    God Bless,Never Bug
"""
from datetime import timedelta, datetime
from functools import wraps

import jwt
from flask import request

from app import bcrypt, config
from tesla_trip_common.models import User
from utils.errors import ValidationError
from utils.error_codes import ErrorCodes


class AuthTool:
    @classmethod
    def sign_in(cls):
        def real_decorator(method, **kwargs):
            @wraps(method)
            def wrapper(*args, **kwargs):
                token = request.headers.get('Authorization')
                if not token:
                    raise ValidationError(error_code=ErrorCodes.TOKEN_MISSING,
                                          error_msg='token missing')
                token_content = cls.decode_access_token(token=token)
                id_ = token_content.get('id')
                user = User.query.filter(
                    User.id == id_
                ).first()
                if not user:
                    raise ValidationError(error_code=ErrorCodes.USER_NOT_EXISTS,
                                          error_msg='user not exist')
                return method(*args, **kwargs, user=user)

            return wrapper

        return real_decorator

    @staticmethod
    def encrypt_password(password):
        return bcrypt.generate_password_hash(password).decode('utf-8')

    @staticmethod
    def decrypt_password(db_password, password):
        return bcrypt.check_password_hash(db_password, password)

    @staticmethod
    def _get_token(expire_time, salt, **kwargs):
        payload = {
            **kwargs,
            'exp': expire_time
        }
        return jwt.encode(payload=payload, key=salt, algorithm='HS256').decode('utf-8')

    @staticmethod
    def _decode(token, salt):
        try:
            return jwt.decode(jwt=token, key=salt, algorithm='HS256')
        except jwt.DecodeError:
            raise ValidationError(error_code=ErrorCodes.INVALID_TOKEN, error_msg='invalid token')
        except jwt.ExpiredSignatureError:
            raise ValidationError(error_code=ErrorCodes.TOKEN_EXPIRED, error_msg='token expired')

    @classmethod
    def get_access_token(cls, **kwargs):
        time_offset = timedelta(seconds=config['ACCESS_TOKEN_EXPIRE_TIME'])
        expire_time = datetime.utcnow() + time_offset
        return cls._get_token(expire_time=expire_time, salt=config['SALT'], **kwargs)

    @classmethod
    def get_refresh_token(cls, **kwargs):
        time_offset = timedelta(seconds=config['REFRESH_TOKEN_EXPIRE_TIME'])
        expire_time = datetime.utcnow() + time_offset
        return cls._get_token(expire_time=expire_time, salt=config['SALT'], **kwargs)

    @classmethod
    def decode_access_token(cls, token):
        return cls._decode(token=token, salt=config['SALT'])

    @classmethod
    def decode_refresh_token(cls, token):
        return cls._decode(token=token, salt=config['SALT'])
