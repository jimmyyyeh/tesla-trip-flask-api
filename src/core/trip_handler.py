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
from tesla_trip_common.models import Trip, Car, SuperCharger
from utils.tools import Tools


class TripHandler:
    @staticmethod
    def get_trips(user_id, page, per_page, charger, start, end, model, spec):
        filter_ = list()
        if user_id:
            filter_.append(Trip.user_id == user_id)
        if charger:
            filter_.append(SuperCharger.id == charger)
        if start:
            filter_.append(Trip.start.like(f'%{start}%'))
        if end:
            filter_.append(Trip.end.like(f'%{end}%'))
        if model:
            filter_.append(Car.model.like(f'%{model}%'))
        if spec:
            filter_.append(Car.spec.like(f'%{spec}%'))
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
            Trip.trip_date,
            Car.model,
            Car.spec,
            Car.manufacture_date,
            SuperCharger.name,
        ).outerjoin(
            Car, Car.id == Trip.car_id
        ).outerjoin(
            SuperCharger, SuperCharger.id == Trip.charger_id
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
                'trip_date': trip.trip_date,
                'car': f'{trip.model}/{trip.spec}/{trip.trip_date.strftime("%F")}',
                'charger': trip.name
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
                charger_id=trip.get('charger_id'),
                charge=trip.get('charge'),
                fee=trip.get('fee'),
                trip_date=trip['trip_date']
            )
            db.session.add(trip_)
        db.session.commit()
