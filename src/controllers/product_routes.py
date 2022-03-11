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
from core.product_handler import ProductHandler
from utils.auth_tool import AuthTool
from utils.const import Const
from utils.response_handler import ResponseHandler


@app.route('/product/<int:product_id>', methods=['GET'])
@app.route('/product', methods=['GET'])
@AuthTool.sign_in()
def get_product(user, product_id=None):
    result = ProductHandler.get_products(product_id=product_id)
    return ResponseHandler.package_result(result=result)


@app.route('/redeem-product/<string:token>', methods=['POST'])
@AuthTool.sign_in(roles=[Const.Role.CHARGER_OWNER])
def redeem_product(user, token):
    result = ProductHandler.redeem_product(
        user=user,
        token=token
    )
    return ResponseHandler.package_result(result=result)
