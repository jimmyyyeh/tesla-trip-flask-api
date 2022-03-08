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

from app import app
from core.user_handler import UserHandler
from utils.auth_tool import AuthTool
from utils.payload_utils import PayloadUtils, PayloadSchema
from utils.response_handler import ResponseHandler


@app.route('/verify', methods=['GET'])
@PayloadUtils.validate()
def verify(payload):
    result = UserHandler.verify(
        verify_token=payload.get('token')
    )
    return ResponseHandler.package_result(result=result)


@app.route('/resend-verify', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.RESEND_VERIFY)
def resend_verify(payload):
    result = UserHandler.resend_verify(
        username=payload['username']
    )
    return ResponseHandler.package_result(result=result)


@app.route('/sign-up', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.SIGN_UP)
def sign_up(payload):
    result = UserHandler.sign_up(
        username=payload['username'],
        password=payload['password'],
        nickname=payload.get('nickname'),
        email=payload['email'],
        birthday=payload['birthday'],
        sex=payload['sex'],
    )
    return ResponseHandler.package_result(result=result)


@app.route('/sign-in', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.SIGN_IN)
def sign_in(payload):
    result = UserHandler.sign_in(
        username=payload['username'],
        password=payload['password']
    )
    return ResponseHandler.package_result(result=result)


@app.route('/profile', methods=['GET'])
@AuthTool.sign_in()
def get_profile(user):
    result = UserHandler.get_profile(
        user=user,
    )
    return ResponseHandler.package_result(result=result)


@app.route('/profile', methods=['PUT'])
@AuthTool.sign_in()
@PayloadUtils.validate(PayloadSchema.UPDATE_PROFILE)
def update_profile(user, payload):
    result = UserHandler.update_profile(
        user_id=user.id,
        nickname=payload.get('nickname'),
        email=payload.get('email'),
    )
    return ResponseHandler.package_result(result=result)


@app.route('/refresh-token', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.REFRESH_TOKEN)
def refresh_token(payload):
    result = UserHandler.refresh_token(
        refresh_token=payload['refresh_token'],
    )
    return ResponseHandler.package_result(result=result)
