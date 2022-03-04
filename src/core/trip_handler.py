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
from tesla_trip_common.models import Trip


class TripHandler:
    @classmethod
    def create_trip(cls, payload):
        for trip in payload:
            trip_ = Trip(
                mileage=trip['mileage'],
                consumption=trip['consumption'],
                total=trip['total'],
                start=trip['start'],
                end=trip['end'],
                start_battery_level=trip['start_battery_level'],
                end_battery_level=trip['end_battery_level'],
                is_charge=trip['is_charge'],
                charge=trip['charge'],
                fee=trip['fee'],
                final_battery_level=trip['final_battery_level']
            )
            db.session.add(trip_)
        db.session.commit()
