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

from app import config

import base64
import qrcode
from io import BytesIO
from secrets import token_hex

from tesla_trip_common.models import Product
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundError
from utils.redis_handler import RedisHandler


class QRCodeHandler:
    @staticmethod
    def decode_product(token):
        content = RedisHandler.get_redeem_product(token=token)
        if not content:
            raise NotFoundError(
                error_msg='content does not exist',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )
        return content

    @staticmethod
    def encode_product(user, product_id):
        product = Product.query.filter(
            Product.id == product_id
        ).first()
        if not product:
            raise NotFoundError(
                error_msg='content does not exist',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )
        content = {
            'user_id': user.id,
            'id': product.id,
            'name': product.name,
            'point': product.point
        }
        token = token_hex(16)
        RedisHandler.set_redeem_product(token=token, content=content)

        url = f'{config["WEB_DOMAIN"]}/redeem/{token}'
        qrcode_ = qrcode.make(url)
        img = BytesIO()
        qrcode_.save(img, format='PNG')
        img = img.getvalue()
        result = {
            'image': base64.b64encode(img).decode()
        }
        return result
