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

from flask import Blueprint
from flasgger import swag_from

from core.trip_handler import TripHandler
from utils.auth_tool import AuthTool
from utils.payload_utils import PayloadUtils, PayloadSchema
from utils.response_handler import ResponseHandler

trip_app = Blueprint('trip', __name__)


@trip_app.route('/', methods=['GET'])
@swag_from('../swagger_yaml/trip/get_trip.yaml')
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


@trip_app.route('/', methods=['POST'])
@swag_from('../swagger_yaml/trip/post_trip.yaml')
@AuthTool.sign_in()
@PayloadUtils.validate(PayloadSchema.CREATE_TRIP)
def create_trip(user, payload):
    result = TripHandler.create_trip(
        user=user,
        payload=payload
    )
    return ResponseHandler.package_result(result=result)
