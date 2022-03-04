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
from tesla_trip_common.models import User
from utils.auth_tool import AuthTool
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundError, ValidationError


class UserHandler:
    @staticmethod
    def sign_in(username, password):
        user = User.query.filter(
            User.username == username
        ).first()
        if not user:
            raise NotFoundError(
                error_msg='user not exist',
                error_code=ErrorCodes.USER_NOT_EXIST
            )
        if not AuthTool.decrypt_password(db_password=user.password, password=password):
            raise ValidationError(
                error_msg='user invalidate',
                error_code=ErrorCodes.USER_INVALIDATE
            )
        result = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'age': user.age,
            'sex': user.sex,
            'email': user.email,
        }
        token = AuthTool.get_access_token(**result)
        refresh_token = AuthTool.get_refresh_token(**result)
        result.update({
            'token': token,
            'refresh_token': refresh_token
        })
        return result
