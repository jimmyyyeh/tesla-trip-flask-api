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
from core.qrcode_handler import QRCodeHandler
from utils.auth_tool import AuthTool
from utils.payload_utils import PayloadUtils, PayloadSchema
from utils.response_handler import ResponseHandler


@app.route('/qrcode/product/<string:token>', methods=['GET'])
@AuthTool.sign_in()
def decode_product(user, token):
    result = QRCodeHandler.decode_product(
        token=token
    )
    return ResponseHandler.package_result(result=result)


@app.route('/qrcode/product', methods=['POST'])
@AuthTool.sign_in()
@PayloadUtils.validate(PayloadSchema.ENCODE_PRODUCT)
def encode_product(user, payload):
    result = QRCodeHandler.encode_product(
        user=user,
        product_id=payload['product_id']
    )
    return ResponseHandler.package_result(result=result)
