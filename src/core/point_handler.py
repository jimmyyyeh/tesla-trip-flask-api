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
from app import db
from tesla_trip_common.models import PointLog


class PointHandler:
    @staticmethod
    def get_deduct_point(trips, trip_rates):
        return trips.count() + trip_rates.count() * 2

    @staticmethod
    def point_change_log(user_id, point, change, type_):
        point_log = PointLog(
            user_id=user_id,
            point=point,
            change=change,
            type=type_
        )
        db.session.add(point_log)
