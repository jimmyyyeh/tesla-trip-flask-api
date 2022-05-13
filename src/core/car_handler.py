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
import base64
from pathlib import Path

from app import db
from core.point_handler import PointHandler
from tesla_trip_common.models import Car, CarModel, Trip, TripRate
from utils.const import Const
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundError
from utils.pattern import Pattern
from utils.tools import Tools


class CarHandler:
    @staticmethod
    def _query_car(user_id, car_id):
        filter_ = [
            Car.user_id == user_id,
        ]
        if car_id:
            filter_.append(Car.id == car_id)
        car = db.session.query(
            Car.id,
            Car.manufacture_date,
            Car.has_image,
            CarModel.model,
            CarModel.spec,
        ).join(
            CarModel, CarModel.id == Car.car_model_id
        ).filter(
            *filter_
        )
        if not car:
            raise NotFoundError(
                error_msg='car does not exists',
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
                'car': f'{car.model}-{car.spec}({Tools.date_to_season(car.manufacture_date)})',
                'model': car.model,
                'spec': car.spec,
                'manufacture_date': car.manufacture_date,
                'has_image': car.has_image
            }
            Tools.serialize_result(dict_=result)
            results.append(result)
        return results

    @staticmethod
    def _save_file(file, id_):
        if not file:
            return None
        _, extension, _, base64_str = Pattern.BASE64.search(file).groups()
        path = './static/image/car'
        filename = f'{id_}.{extension}'
        Path(path).mkdir(parents=True, exist_ok=True)
        with open(f'{path}/{filename}', 'wb') as f:
            f.write(base64.decodebytes(base64_str.encode()))
        return filename

    @classmethod
    def create_car(cls, user_id, model, spec, manufacture_date, file):
        car_model = CarModel.query.filter(
            CarModel.model == model,
            CarModel.spec == spec
        ).first()
        
        if not car_model:
            raise NotFoundError(
                error_msg='car model does not exists',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )
        car = Car(
            user_id=user_id,
            car_model_id=car_model.id,
            manufacture_date=manufacture_date,
            has_image=True if file else False
        )
        db.session.add(car)
        db.session.flush()
        cls._save_file(file=file, id_=car.id)
        db.session.commit()
        result = {
            'id': car.id,
            'model': car_model.model,
            'spec': car_model.spec,
            'manufacture_date': car.manufacture_date,
            'has_image': car.has_image
        }
        Tools.serialize_result(dict_=result)
        return result

    @classmethod
    def update_car(cls, user_id, car_id, model, spec, manufacture_date):
        car = Car.query.filter(
            Car.id == car_id,
            Car.user_id == user_id
        ).first()
        if not car:
            raise NotFoundError(
                error_msg='car does not exists',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )
        car_model = CarModel.query.filter(
            CarModel.model == model,
            CarModel.spec == spec
        ).first()
        if not car_model:
            raise NotFoundError(
                error_msg='car model does not exists',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )
        car.car_model_id = car_model.id
        car.manufacture_date = manufacture_date
        db.session.commit()
        result = {
            'id': car.id,
            'model': car_model.model,
            'spec': car_model.spec,
            'manufacture_date': car.manufacture_date,
            'has_image': car.has_image
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
        if trip_rates.all():
            trip_rates.delete()
        if trips.all():
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

    @classmethod
    def get_car_models(cls):
        car_models = CarModel.query.all()
        results = list()
        for car_model in car_models:
            result = {
                'id': car_model.id,
                'model': car_model.model,
                'spec': car_model.spec,
            }
            results.append(result)
        return results
