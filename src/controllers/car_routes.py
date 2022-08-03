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

from flask import Blueprint
from flasgger import swag_from

from core.car_handler import CarHandler
from utils.auth_tool import AuthTool
from utils.payload_utils import PayloadUtils, PayloadSchema
from utils.response_handler import ResponseHandler

car_app = Blueprint('car', __name__)


@car_app.route('/<int:car_id>', endpoint='get_car_with_car_id', methods=['GET'])
@car_app.route('', endpoint='get_car_without_car_id', methods=['GET'])
@swag_from('../swagger_yaml/car/get_car_without_id.yaml', endpoint='get_car_without_car_id')
@swag_from('../swagger_yaml/car/get_car_with_id.yaml', endpoint='get_car_with_car_id')
@AuthTool.sign_in()
def get_car(user, car_id=None):
    result = CarHandler.get_cars(
        user_id=user.id,
        car_id=car_id
    )
    return ResponseHandler.package_result(result=result)


@car_app.route('', methods=['POST'])
@swag_from('../swagger_yaml/car/post_car.yaml')
@AuthTool.sign_in()
@PayloadUtils.validate(PayloadSchema.CREATE_CAR)
def create_car(user, payload):
    result = CarHandler.create_car(
        user_id=user.id,
        model=payload['model'],
        spec=payload['spec'],
        manufacture_date=payload['manufacture_date'],
        file=payload.get('file')
    )
    return ResponseHandler.package_result(result=result)


@car_app.route('/<int:car_id>', methods=['PUT'])
@swag_from('../swagger_yaml/car/put_car.yaml')
@AuthTool.sign_in()
@PayloadUtils.validate(PayloadSchema.UPDATE_CAR)
def update_car(user, car_id, payload):
    result = CarHandler.update_car(
        user_id=user.id,
        car_id=car_id,
        model=payload['model'],
        spec=payload['spec'],
        manufacture_date=payload['manufacture_date']
    )
    return ResponseHandler.package_result(result=result)


@car_app.route('/<int:car_id>', methods=['DELETE'])
@swag_from('../swagger_yaml/car/delete_car.yaml')
@AuthTool.sign_in()
def delete_car(user, car_id):
    result = CarHandler.delete_car(
        user=user,
        car_id=car_id,
    )
    return ResponseHandler.package_result(result=result)


@car_app.route('/deduct-point/<int:car_id>', methods=['GET'])
@AuthTool.sign_in()
def get_car_deduct_point(user, car_id):
    result = CarHandler.get_car_deduct_point(
        user=user,
        car_id=car_id,
    )
    return ResponseHandler.package_result(result=result)


@car_app.route('/car-model', methods=['GET'])
@swag_from('../swagger_yaml/car/get_car_model.yaml')
@AuthTool.sign_in()
def get_car_model(user):
    result = CarHandler.get_car_models()
    return ResponseHandler.package_result(result=result)
