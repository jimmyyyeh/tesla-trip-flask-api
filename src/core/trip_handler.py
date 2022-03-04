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
from tesla_trip_common.models import Trip, Car
from utils.tools import Tools


class TripHandler:
    @staticmethod
    def get_trips(user_id, page, per_page):
        filter_ = list()
        if user_id:
            filter_.append(Trip.user_id == user_id)
        trips = db.session.query(
            Trip.id,
            Trip.mileage,
            Trip.consumption,
            Trip.total,
            Trip.start,
            Trip.start_battery_level,
            Trip.end,
            Trip.end_battery_level,
            Trip.is_charge,
            Trip.charge,
            Trip.fee,
            Trip.final_battery_level,
            Trip.trip_date,
            Car.model,
            Car.spec,
            Car.manufacture_date
        ).outerjoin(
            Car, Car.id == Trip.car_id
        ).filter(
            *filter_
        ).paginate(
            page=page,
            per_page=per_page
        )
        pager = Tools.make_pager(
            page=page,
            per_page=per_page,
            objs=trips
        )
        results = list()
        for trip in trips.items:
            result = {
                'id': trip.id,
                'mileage': trip.mileage,
                'consumption': trip.consumption,
                'total': trip.total,
                'start': trip.start,
                'end': trip.end,
                'start_battery_level': trip.start_battery_level,
                'end_battery_level': trip.end_battery_level,
                'is_charge': trip.is_charge,
                'charge': trip.charge,
                'fee': trip.fee,
                'final_battery_level': trip.final_battery_level,
                'trip_date': trip.trip_date,
                'car': f'{trip.model}/{trip.spec}/{trip.trip_date.strftime("%F")}'
            }
            Tools.serialize_result(dict_=result)
            results.append(result)
        return results, pager

    @staticmethod
    def create_trip(user_id, payload):
        for trip in payload:
            trip_ = Trip(
                user_id=user_id,
                car_id=trip['car_id'],
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
                final_battery_level=trip['final_battery_level'],
                trip_date=trip['trip_date']
            )
            db.session.add(trip_)
        db.session.commit()
