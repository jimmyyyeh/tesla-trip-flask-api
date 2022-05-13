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

from app import app
from core.car_handler import CarHandler
from utils.auth_tool import AuthTool
from utils.payload_utils import PayloadUtils, PayloadSchema
from utils.response_handler import ResponseHandler


@app.route('/car/<int:car_id>', methods=['GET'])
@app.route('/car', methods=['GET'])
@AuthTool.sign_in()
def get_car(user, car_id=None):
    result = CarHandler.get_cars(
        user_id=user.id,
        car_id=car_id
    )
    return ResponseHandler.package_result(result=result)


@app.route('/car', methods=['POST'])
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


@app.route('/car/<int:car_id>', methods=['PUT'])
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


@app.route('/car/<int:car_id>', methods=['DELETE'])
@AuthTool.sign_in()
def delete_car(user, car_id):
    result = CarHandler.delete_car(
        user=user,
        car_id=car_id,
    )
    return ResponseHandler.package_result(result=result)


@app.route('/car/deduct-point/<int:car_id>', methods=['GET'])
@AuthTool.sign_in()
def get_car_deduct_point(user, car_id):
    result = CarHandler.get_car_deduct_point(
        user=user,
        car_id=car_id,
    )
    return ResponseHandler.package_result(result=result)


@app.route('/car/car-model', methods=['GET'])
def get_car_model():
    result = CarHandler.get_car_models()
    return ResponseHandler.package_result(result=result)
