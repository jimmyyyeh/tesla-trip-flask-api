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
from utils.payload_utils import PayloadUtils, PayloadSchema
from utils.response_handler import ResponseHandler


@app.route('/sign-up', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.SIGN_UP)
def sign_up(payload):
    result = UserHandler.sign_up(
        username=payload['username'],
        password=payload['password'],
        nickname=payload.get('nickname'),
        email=payload['email'],
        age=payload['age'],
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


@app.route('/refresh-token', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.REFRESH_TOKEN)
def refresh_token(payload):
    result = UserHandler.refresh_token(
        refresh_token=payload['refresh_token'],
    )
    return ResponseHandler.package_result(result=result)
