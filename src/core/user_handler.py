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
from app import db
from tesla_trip_common.models import User
from utils.auth_tool import AuthTool
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundError, ValidationError
from utils.tools import Tools


class UserHandler:
    @staticmethod
    def sign_up(username, password, nickname, email, birthday, sex):
        user = User.query.filter(
            User.username == username
        ).first()
        if user:
            raise ValidationError(
                error_msg='username already exists',
                error_code=ErrorCodes.USER_ALREADY_EXIST
            )
        user = User(
            username=username,
            password=AuthTool.encrypt_password(password=password),
            nickname=nickname or username,
            email=email,
            birthday=birthday,
            sex=sex,
        )
        db.session.add(user)
        db.session.commit()
        result = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'birthday': user.birthday,
            'sex': user.sex,
            'email': user.email,
        }
        Tools.serialize_result(dict_=result)
        return result

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
            'birthday': user.birthday,
            'sex': user.sex,
            'email': user.email,
        }
        Tools.serialize_result(dict_=result)
        token = AuthTool.get_access_token(**result)
        refresh_token = AuthTool.get_refresh_token(**result)
        result.update({
            'token': token,
            'refresh_token': refresh_token
        })
        return result

    @staticmethod
    def update_profile(user_id, nickname, email):
        user = User.query.filter(
            User.id == user_id
        ).first()
        if not user:
            raise NotFoundError(
                error_msg='user not exist',
                error_code=ErrorCodes.USER_NOT_EXIST
            )
        if nickname:
            user.nickname = nickname
        if email:
            user.email = email
        db.session.commit()
        result = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'birthday': user.birthday,
            'sex': user.sex,
            'email': user.email,
        }
        Tools.serialize_result(dict_=result)
        token = AuthTool.get_access_token(**result)
        refresh_token = AuthTool.get_refresh_token(**result)
        result.update({
            'token': token,
            'refresh_token': refresh_token
        })
        return result

    @staticmethod
    def refresh_token(refresh_token):
        result = AuthTool.decode_refresh_token(token=refresh_token)
        token = AuthTool.get_access_token(**result)
        refresh_token = AuthTool.get_refresh_token(**result)
        result.update({
            'token': token,
            'refresh_token': refresh_token
        })
        return result
