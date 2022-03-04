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
    })

    CREATE_CAR = Schema({
        'model': str,
        'spec': str,
        'manufacture_date': str,
    })

    UPDATE_CAR = Schema({
        'model': str,
        'spec': str,
        'manufacture_date': str,
    })

    TRIP = Schema({
        'mileage': int,
        'consumption': Or(float, int),
        'total': Or(float, int),
        'start': str,
        'end': str,
        'start_battery_level': int,
        'end_battery_level': int,
        'is_charge': bool,
        'charge': Or(int, None),
        'fee': Or(float, int, None),
        'final_battery_level': int,
    })

    CREATE_TRIP = Schema(
        And(list, lambda x: list(map(PayloadSchema.TRIP.validate, x))),
    )
