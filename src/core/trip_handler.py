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
from datetime import datetime, timedelta

from sqlalchemy import func

from app import db
from tesla_trip_common.models import Trip, Car, SuperCharger, TripRate
from utils.tools import Tools


class TripHandler:
    @staticmethod
    def get_trips(user_id, is_my_trip, page, per_page, charger, start, end, model, spec):
        now_ = datetime.now()
        filter_ = [
            Trip.create_datetime >= now_ - timedelta(days=365),
        ]
        # 限制近一年 避免資料太多
        if is_my_trip:
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

        trip_rate_count = db.session.query(
            TripRate.trip_id.label('trip_id'),
            func.count(TripRate.trip_id).label('trip_rate_count')
        ).group_by(
            TripRate.trip_id
        ).subquery()

        is_rate = db.session.query(
            TripRate.id.label('is_rate'),
            TripRate.trip_id.label('trip_id')
        ).filter(
            TripRate.user_id == user_id
        ).subquery()

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
            trip_rate_count.c.trip_rate_count,
            is_rate.c.is_rate,
            Car.model,
            Car.spec,
            Car.manufacture_date,
            SuperCharger.name,
        ).outerjoin(
            Car, Car.id == Trip.car_id
        ).outerjoin(
            SuperCharger, SuperCharger.id == Trip.charger_id
        ).outerjoin(
            trip_rate_count, trip_rate_count.c.trip_id == Trip.id
        ).outerjoin(
            is_rate, is_rate.c.trip_id == Trip.id
        ).filter(
            *filter_
        ).order_by(
            Trip.create_datetime.desc()
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
                'car': f'{trip.model}-{trip.spec}({Tools.date_to_season(trip.trip_date)})',
                'charger': trip.name,
                'trip_rate_count': trip.trip_rate_count,
                'is_rate': True if trip.is_rate else False
            }
            Tools.serialize_result(dict_=result)
            results.append(result)
        return results, pager

    @staticmethod
    def create_trip(user, payload):
        for trip in payload:
            trip_ = Trip(
                user_id=user.id,
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
            user.point += 1
        db.session.commit()
        return True

    @staticmethod
    def update_user_trip_rate(user_id, trip_id):
        filter_ = [
            TripRate.trip_id == trip_id,
            TripRate.user_id == user_id
        ]
        trip_rate = TripRate.query.filter(
            *filter_
        )
        if not trip_rate.first():
            trip_rate = TripRate(
                user_id=user_id,
                trip_id=trip_id
            )
            db.session.add(trip_rate)
        else:
            trip_rate.delete()
        db.session.commit()
        return True
