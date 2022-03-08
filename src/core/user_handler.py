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

from secrets import token_hex
from threading import Thread

from sqlalchemy import or_

from app import app, db, config
from tesla_trip_common.models import User
from utils.auth_tool import AuthTool
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundError, ValidationError
from utils.redis_handler import RedisHandler
from utils.tools import Tools
from utils.mail_handler import MailHandler


class UserHandler:
    @staticmethod
    def _send_verify_mail(email, id_):
        verify_token = token_hex(16)
        RedisHandler.set_verify_user(
            verify_token=verify_token,
            id_=id_
        )
        html = f"""
                <h1>歡迎註冊</h1>
                <body>
                    <p>歡迎您註冊Tesla Trip，請點選以下連結以進行驗證:</p>
                    <a href='{config['WEB_DOMAIN']}/verify/{verify_token}'>驗證連結</a>
                </body>
                """
        with app.app_context():
            MailHandler.send_mail(
                title='Tesla Trip 驗證信件',
                recipients=[email],
                html=html
            )

    @staticmethod
    def verify(verify_token):
        id_ = RedisHandler.get_verify_user(
            verify_token=verify_token
        )
        if not id_:
            raise ValidationError(
                error_msg='verify token not exists',
                error_code=ErrorCodes.VERIFY_TOKEN_NOT_EXISTS
            )
        user = User.query.filter(
            User.id == id_
        ).first()
        if not user:
            raise NotFoundError(
                error_msg='user not exists',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        user.is_verified = True
        db.session.commit()
        return True

    @classmethod
    def resend_verify(cls, username):
        user = User.query.filter(
            User.username == username
        ).first()
        if not user:
            raise NotFoundError(
                error_msg='user not exists',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        thread = Thread(
            target=cls._send_verify_mail,
            args=(user.email, user.id,)
        )
        thread.start()
        return True

    @classmethod
    def sign_up(cls, username, password, nickname, email, birthday, sex):

        user = User.query.filter(
            or_(User.username == username,
                User.email == email)
        ).first()
        if user:
            raise ValidationError(
                error_msg='username already exists',
                error_code=ErrorCodes.USER_ALREADY_EXISTS
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
        db.session.flush()
        result = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'birthday': user.birthday,
            'sex': user.sex,
            'email': user.email,
            'point': user.point,
            'is_verified': user.is_verified,
        }
        Tools.serialize_result(dict_=result)
        thread = Thread(
            target=cls._send_verify_mail,
            args=(email, user.id,)
        )
        thread.start()
        db.session.commit()
        return result

    @staticmethod
    def sign_in(username, password):
        user = User.query.filter(
            User.username == username
        ).first()
        if not user:
            raise NotFoundError(
                error_msg='user not exists',
                error_code=ErrorCodes.USER_NOT_EXISTS
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
            'point': user.point,
            'is_verified': user.is_verified,
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
    def get_profile(user):
        result = {
            'id': user.id,
            'username': user.username,
            'nickname': user.nickname,
            'birthday': user.birthday,
            'sex': user.sex,
            'email': user.email,
            'point': user.point,
            'is_verified': user.is_verified,
        }
        Tools.serialize_result(dict_=result)
        return result

    @staticmethod
    def update_profile(user_id, nickname, email):
        user = User.query.filter(
            User.id == user_id
        ).first()
        if not user:
            raise NotFoundError(
                error_msg='user not exists',
                error_code=ErrorCodes.USER_NOT_EXISTS
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
            'point': user.point,
            'is_verified': user.is_verified,
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

    @staticmethod
    def _send_reset_password_mail(email, id_):
        reset_token = token_hex(16)
        RedisHandler.set_reset_password(
            reset_token=reset_token,
            id_=id_,
        )
        html = f"""
                <h1>重設密碼</h1>
                <body>
                    <p>親愛的Tesla Trip用戶您好，請點選以下連結以進行重置密碼:</p>
                    <a href='{config['WEB_DOMAIN']}/resetPassword/{reset_token}'>重設密碼連結</a>
                </body>
                """
        with app.app_context():
            MailHandler.send_mail(
                title='Tesla Trip 忘記密碼',
                recipients=[email],
                html=html
            )

    @classmethod
    def request_reset_password(cls, email):
        user = User.query.filter(
            User.email == email
        ).first()
        if not user:
            raise NotFoundError(
                error_msg='user not exists',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        thread = Thread(
            target=cls._send_reset_password_mail,
            args=(email, user.id)
        )
        thread.start()
        return True

    @staticmethod
    def reset_password(reset_token, username, password):
        id_ = RedisHandler.get_reset_password(
            reset_token=reset_token
        )
        if not id_:
            raise ValidationError(
                error_msg='reset password token not exists',
                error_code=ErrorCodes.RESET_PASSWORD_TOKEN_NOT_EXISTS
            )
        user = User.query.filter(
            User.id == id_
        ).first()
        if not user:
            raise NotFoundError(
                error_msg='user not exists',
                error_code=ErrorCodes.USER_NOT_EXISTS
            )
        if user.username != username:
            raise NotFoundError(
                error_msg='reset password token invalidated',
                error_code=ErrorCodes.RESET_PASSWORD_TOKEN_INVALIDATE
            )
        user.password = AuthTool.encrypt_password(password=password)
        db.session.commit()
        return True
