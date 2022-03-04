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

import jwt

from app import bcrypt, config
from utils.errors import ValidationError
from utils.error_codes import ErrorCodes


class AuthTool:
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
            raise ValidationError(error_code=ErrorCodes.INVALID_ACCESS_TOKEN)
        except jwt.ExpiredSignatureError:
            raise ValidationError(error_code=ErrorCodes.ACCESS_TOKEN_IS_EXPIRED)

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
