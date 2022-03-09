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


@app.route('/trip', methods=['GET'])
@AuthTool.sign_in()
@PayloadUtils.validate()
def get_trip(user, payload):
    result, pager = TripHandler.get_trips(
        user_id=user.id,
        is_my_trip=int(payload.get('is_my_trip', 0)),
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


@app.route('/trip-rate', methods=['POST'])
@AuthTool.sign_in()
@PayloadUtils.validate(PayloadSchema.UPDATE_TRIP_RATE)
def update_trip_rate(user, payload):
    result = TripHandler.update_user_trip_rate(
        user_id=user.id,
        trip_id=payload['trip_id']
    )
    return ResponseHandler.package_result(result=result)
