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
from core.point_handler import PointHandler
from tesla_trip_common.models import Car, Trip, TripRate
from utils.const import Const
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundError
from utils.tools import Tools


class CarHandler:
    @staticmethod
    def _query_car(user_id, car_id):
        filter_ = [
            Car.user_id == user_id,
        ]
        if car_id:
            filter_.append(Car.id == car_id)
        car = Car.query.filter(
            *filter_
        )
        if not car:
            raise NotFoundError(
                error_msg='data is not exists',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )
        return car

    @classmethod
    def get_cars(cls, user_id, car_id):
        cars = cls._query_car(user_id=user_id, car_id=car_id)
        cars = cars.all()
        results = list()
        for car in cars:
            result = {
                'id': car.id,
                'model': car.model,
                'spec': car.spec,
                'manufacture_date': car.manufacture_date
            }
            Tools.serialize_result(dict_=result)
            results.append(result)
        return results

    @staticmethod
    def create_car(user_id, model, spec, manufacture_date):
        car = Car(
            user_id=user_id,
            model=model,
            spec=spec,
            manufacture_date=manufacture_date
        )
        db.session.add(car)
        db.session.commit()
        result = {
            'id': car.id,
            'model': car.model,
            'spec': car.spec,
            'manufacture_date': car.manufacture_date
        }
        Tools.serialize_result(dict_=result)
        return result

    @classmethod
    def update_car(cls, user_id, car_id, model, spec, manufacture_date):
        car = cls._query_car(user_id=user_id, car_id=car_id)
        car = car.first()
        car.model = model
        car.spec = spec
        car.manufacture_date = manufacture_date
        db.session.commit()
        result = {
            'id': car.id,
            'model': car.model,
            'spec': car.spec,
            'manufacture_date': car.manufacture_date
        }
        Tools.serialize_result(dict_=result)
        return result

    @staticmethod
    def _deduct_point(user, trips, trip_rates):
        origin_point = user.point
        total_deduct = PointHandler.get_deduct_point(trips=trips, trip_rates=trip_rates)
        if origin_point < total_deduct:
            user.point = 0
            deduct_point = origin_point
        else:
            user.point -= total_deduct
            deduct_point = user.point
        PointHandler.point_change_log(
            user_id=user.id,
            point=origin_point,
            change=deduct_point,
            type_=Const.PointLogType.DELETE_CAR,
        )

    @classmethod
    def _get_delete_car_info(cls, user_id, car_id):
        trips = Trip.query.filter(
            Trip.car_id == car_id
        )
        trip_ids = {trip.id for trip in trips}
        trip_rates = TripRate.query.filter(
            TripRate.trip_id.in_(trip_ids)
        )
        cars = cls._query_car(user_id=user_id, car_id=car_id)
        return cars, trips, trip_rates

    @classmethod
    def delete_car(cls, user, car_id):
        cars, trips, trip_rates = cls._get_delete_car_info(user_id=user.id, car_id=car_id)
        trip_rates.delete()
        trips.delete()
        cars.delete()
        cls._deduct_point(user=user, trips=trips, trip_rates=trip_rates)
        db.session.commit()
        return True

    @classmethod
    def get_car_deduct_point(cls, user, car_id):
        _, trips, trip_rates = cls._get_delete_car_info(user_id=user.id, car_id=car_id)
        total_deduct = PointHandler.get_deduct_point(trips=trips, trip_rates=trip_rates)
        return {'total': total_deduct}
