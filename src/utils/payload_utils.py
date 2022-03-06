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

from functools import wraps

from flask import request
from schema import Schema, Optional, Or, And

from utils.const import Const


class PayloadUtils:
    @staticmethod
    def validate(schema=None):
        def real_decorator(method, **kwargs):
            @wraps(method)
            def wrapper(*args, **kwargs):
                if request.method in {'GET', 'DELETE'}:
                    payload = request.args
                    payload = dict(payload)
                else:
                    payload = dict(request.form) or request.get_json(force=True)
                if schema:
                    schema.validate(payload)
                return method(*args, **kwargs, payload=payload)

            return wrapper

        return real_decorator


class PayloadSchema:
    SIGN_IN = Schema({
        'username': str,
        'password': str,
    }, ignore_extra_keys=True)

    SIGN_UP = Schema({
        'username': str,
        'password': str,
        Optional('nickname'): Or(str, None),
        'email': str,
        'birthday': str,
        'sex': And(str, lambda x: x in Const.Sex.get_elements()),
    }, ignore_extra_keys=True)

    UPDATE_PROFILE = Schema({
        Optional('email'): Or(str, None),
        Optional('nickname'): Or(str, None),
    }, ignore_extra_keys=True)

    REFRESH_TOKEN = Schema({
        'refresh_token': str,
    }, ignore_extra_keys=True)

    CREATE_CAR = Schema({
        'model': str,
        'spec': str,
        'manufacture_date': str,
    }, ignore_extra_keys=True)

    UPDATE_CAR = Schema({
        'model': str,
        'spec': str,
        'manufacture_date': str,
    }, ignore_extra_keys=True)

    TRIP = Schema({
        'car_id': int,
        'mileage': int,
        'consumption': Or(float, int),
        'total': Or(float, int),
        'start': str,
        'end': str,
        'start_battery_level': int,
        'end_battery_level': int,
        'is_charge': bool,
        Optional('charger_id'): Or(int, None),
        Optional('charge'): Or(int, None),
        Optional('fee'): Or(float, int, None),
        'trip_date': str,
    }, ignore_extra_keys=True)

    CREATE_TRIP = Schema(
        And(list, lambda x: list(map(PayloadSchema.TRIP.validate, x))),
    )
