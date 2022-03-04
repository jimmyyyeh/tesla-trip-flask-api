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
from utils.payload_utils import PayloadUtils, PayloadSchema
from utils.response_handler import ResponseHandler


@app.route('/trip', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.CREATE_TRIP)
def create_trip(payload):
    result = TripHandler.create_trip(
        payload=payload
    )
    return ResponseHandler.package_result(result=result)
