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


@app.route('/trip/<int:user_id>', methods=['GET'])
@app.route('/trip', methods=['GET'])
@AuthTool.sign_in()
@PayloadUtils.validate()
def get_trip(user, payload, user_id=None):
    result, pager = TripHandler.get_trips(
        user_id=user_id,
        page=int(payload.get('page', 1)),
        per_page=int(payload.get('per_page', 10)),
        charger=payload.get('charger'),
        start=payload.get('start'),
        end=payload.get('end'),
        model=payload.get('model'),
        spec=payload.get('spec'),
    )
    return ResponseHandler.package_result(result=result, pager=pager)


@app.route('/trip', methods=['POST'])
@AuthTool.sign_in()
@PayloadUtils.validate(PayloadSchema.CREATE_TRIP)
def create_trip(user, payload):
    result = TripHandler.create_trip(
        user=user,
        payload=payload
    )
    return ResponseHandler.package_result(result=result)
