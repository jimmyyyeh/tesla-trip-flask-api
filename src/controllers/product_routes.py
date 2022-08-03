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

from core.product_handler import ProductHandler
from utils.auth_tool import AuthTool
from utils.const import Const
from utils.payload_utils import PayloadUtils, PayloadSchema
from utils.response_handler import ResponseHandler

product_app = Blueprint('product', __name__)


@product_app.route('/<int:product_id>', methods=['GET'])
@product_app.route('', methods=['GET'])
@PayloadUtils.validate()
@AuthTool.sign_in()
def get_product(user, payload, product_id=None):
    result, pager = ProductHandler.get_products(
        user=user,
        product_id=product_id,
        is_self=int(payload.get('is_self', 0)),
        charger_id=payload.get('charger_id'),
        name=payload.get('name'),
        page=int(payload.get('page', 1)),
        per_page=int(payload.get('per_page', 10)),
    )
    return ResponseHandler.package_result(result=result, pager=pager)


@product_app.route('', methods=['POST'])
@PayloadUtils.validate(PayloadSchema.CREATE_PRODUCT)
@AuthTool.sign_in([Const.Role.CHARGER_OWNER])
def create_product(user, payload):
    result = ProductHandler.create_product(
        user=user,
        name=payload['name'],
        stock=payload['stock'],
        point=payload['point'],
        is_launched=payload['is_launched'],
    )
    return ResponseHandler.package_result(result=result)


@product_app.route('/<int:product_id>', methods=['PUT'])
@PayloadUtils.validate(PayloadSchema.UPDATE_PRODUCT)
@AuthTool.sign_in([Const.Role.CHARGER_OWNER])
def update_product(user, payload, product_id):
    result = ProductHandler.update_product(
        user=user,
        product_id=product_id,
        name=payload.get('name'),
        stock=payload.get('stock'),
        point=payload.get('point'),
        is_launched=payload.get('is_launched'),
    )
    return ResponseHandler.package_result(result=result)


@product_app.route('/<int:product_id>', methods=['DELETE'])
@AuthTool.sign_in([Const.Role.CHARGER_OWNER])
def delete_product(user, product_id):
    result = ProductHandler.delete_product(
        user=user,
        product_id=product_id,
    )
    return ResponseHandler.package_result(result=result)


@product_app.route('/redeem-product/<string:token>', methods=['POST'])
@AuthTool.sign_in(Const.Role.CHARGER_OWNER)
def redeem_product(user, token):
    result = ProductHandler.redeem_product(
        user=user,
        token=token
    )
    return ResponseHandler.package_result(result=result)
