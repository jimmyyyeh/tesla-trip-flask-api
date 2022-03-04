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
from core.trip_handler import TripHandler
from utils.auth_tool import AuthTool
from utils.payload_utils import PayloadUtils, PayloadSchema
from utils.response_handler import ResponseHandler


@app.route('/trip', methods=['POST'])
@AuthTool.sign_in()
@PayloadUtils.validate(PayloadSchema.CREATE_TRIP)
def create_trip(user, payload):
    result = TripHandler.create_trip(
        user_id=user.id,
        payload=payload
    )
    return ResponseHandler.package_result(result=result)
