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

from flasgger import swag_from

from app import app
from core.user_handler import UserHandler
from utils.auth_tool import AuthTool
from utils.payload_utils import PayloadUtils, PayloadSchema
from utils.response_handler import ResponseHandler


@app.route('/verify', methods=['POST'])
@swag_from('../swagger_yaml/user/post_verify.yaml')
@PayloadUtils.validate(PayloadSchema.VERIFY)
def verify(payload):
    result = UserHandler.verify(
        verify_token=payload['token']
    )
    return ResponseHandler.package_result(result=result)


@app.route('/resend-verify', methods=['POST'])
@swag_from('../swagger_yaml/user/post_resend_verify.yaml')
@PayloadUtils.validate(PayloadSchema.RESEND_VERIFY)
def resend_verify(payload):
    result = UserHandler.resend_verify(
        username=payload['username']
    )
    return ResponseHandler.package_result(result=result)


@app.route('/sign-up', methods=['POST'])
@swag_from('../swagger_yaml/user/post_sign_up.yaml')
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
@swag_from('../swagger_yaml/user/post_sign_in.yaml')
@PayloadUtils.validate(PayloadSchema.SIGN_IN)
def sign_in(payload):
    result = UserHandler.sign_in(
        username=payload['username'],
        password=payload['password']
    )
    return ResponseHandler.package_result(result=result)


@app.route('/profile', methods=['GET'])
@swag_from('../swagger_yaml/user/get_profile.yaml')
@AuthTool.sign_in()
def get_profile(user):
    result = UserHandler.get_profile(
        user=user,
    )
    return ResponseHandler.package_result(result=result)


@app.route('/profile', methods=['PUT'])
@AuthTool.sign_in()
@PayloadUtils.validate(PayloadSchema.UPDATE_PROFILE)
@swag_from('../swagger_yaml/user/put_profile.yaml')
def update_profile(user, payload):
    result = UserHandler.update_profile(
        user_id=user.id,
        nickname=payload.get('nickname'),
        email=payload.get('email'),
    )
    return ResponseHandler.package_result(result=result)


@app.route('/refresh-token', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.REFRESH_TOKEN)
@swag_from('../swagger_yaml/user/post_refresh_token.yaml')
def refresh_token(payload):
    result = UserHandler.refresh_token(
        refresh_token=payload['refresh_token'],
    )
    return ResponseHandler.package_result(result=result)


@app.route('/request-reset-password', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.REQUEST_RESET_PASSWORD)
@swag_from('../swagger_yaml/user/post_request_reset_password.yaml')
def request_reset_password(payload):
    result = UserHandler.request_reset_password(
        email=payload['email'],
    )
    return ResponseHandler.package_result(result=result)


@app.route('/reset-password', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.RESET_PASSWORD)
@swag_from('../swagger_yaml/user/post_reset_password.yaml')
def reset_password(payload):
    result = UserHandler.reset_password(
        reset_token=payload['token'],
        username=payload['username'],
        password=payload['password']
    )
    return ResponseHandler.package_result(result=result)
