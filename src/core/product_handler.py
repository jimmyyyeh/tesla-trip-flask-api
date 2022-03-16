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
from tesla_trip_common.models import Product, SuperCharger, User, RedeemLog
from utils.const import Const
from utils.error_codes import ErrorCodes
from utils.errors import NotFoundError, ValidationError
from utils.redis_handler import RedisHandler


class ProductHandler:
    @staticmethod
    def get_products(user, product_id, is_self):
        filter_ = []
        if product_id:
            filter_.append(Product.id == product_id)
        if is_self:
            filter_.append(SuperCharger.id == user.charger_id)
        products = db.session.query(
            Product.id,
            Product.name,
            Product.stock,
            Product.point,
            SuperCharger.name.label('charger')
        ).join(
            SuperCharger, SuperCharger.id == Product.charger_id
        ).filter(
            *filter_
        ).all()
        results = list()
        for product in products:
            result = {
                'id': product.id,
                'name': product.name,
                'stock': product.stock,
                'point': product.point
            }
            results.append(result)
        return results

    @staticmethod
    def _redeem_log(seller_id, buyer_id, product_id):
        redeem_log = RedeemLog(
            seller_id=seller_id,
            buyer_id=buyer_id,
            product_id=product_id,
        )
        db.session.add(redeem_log)

    @classmethod
    def redeem_product(cls, user, token):
        content = RedisHandler.get_redeem_product(token=token)
        if not content:
            raise NotFoundError(
                error_msg='content does not exists',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )
        buyer_id = content['user_id']
        product_id = content['id']
        product_point = content['point']
        seller = user
        buyer = User.query.filter(
            User.id == buyer_id
        ).first()

        origin_point = buyer.point
        if origin_point < product_point:
            raise ValidationError(
                error_msg='insufficient point',
                error_code=ErrorCodes.INSUFFICIENT_POINT
            )
        buyer.point -= product_point
        cls._redeem_log(seller_id=seller.id, buyer_id=buyer_id, product_id=product_id)
        PointHandler.point_change_log(
            user_id=buyer.id,
            point=origin_point,
            change=product_point,
            type_=Const.PointLogType.REDEEM_PRODUCT
        )
        db.session.commit()
        RedisHandler.delete_redeem_product(token=token)
        return True
