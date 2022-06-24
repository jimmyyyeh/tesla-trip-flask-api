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
from utils.tools import Tools


class ProductHandler:
    @staticmethod
    def get_products(user, product_id, is_self, charger_id, name, page, per_page):
        filter_ = []
        if product_id:
            filter_.append(Product.id == product_id)
        if is_self:
            filter_.append(SuperCharger.id == user.charger_id)
        if charger_id:
            filter_.append(SuperCharger.id == charger_id)
        if name:
            filter_.append(Product.name.like(f'%{name}%'))
        products = db.session.query(
            Product.id,
            Product.name,
            Product.stock,
            Product.point,
            Product.is_launched,
            SuperCharger.name.label('charger')
        ).join(
            SuperCharger, SuperCharger.id == Product.charger_id
        ).filter(
            *filter_
        ).paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        pager = Tools.make_pager(
            page=page,
            per_page=per_page,
            objs=products
        )

        results = list()
        for product in products.items:
            result = {
                'id': product.id,
                'name': product.name,
                'stock': product.stock,
                'point': product.point,
                'is_launched': product.is_launched
            }
            results.append(result)
        return results, pager

    @staticmethod
    def create_product(user, name, stock, point, is_launched):
        product = Product(
            name=name,
            stock=stock,
            point=point,
            is_launched=is_launched,
            charger_id=user.charger_id,
        )
        db.session.add(product)
        db.session.commit()
        result = {
            'id': product.id,
            'name': product.name,
            'stock': product.stock,
            'point': product.point,
            'is_launched': product.is_launched
        }
        return result

    @staticmethod
    def _query_product(charger_id, product_id):
        product = Product.query.filter(
            Product.id == product_id,
            Product.charger_id == charger_id
        )
        if not product.first():
            raise NotFoundError(
                error_msg='product does not exist',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )
        return product

    @classmethod
    def update_product(cls, user, product_id, name, stock, point, is_launched):
        product = cls._query_product(charger_id=user.charger_id, product_id=product_id)
        product = product.first()
        if name:
            product.name = name
        if stock:
            product.stock = stock
        if point:
            product.point = point
        if is_launched:
            product.is_launched = is_launched
        db.session.commit()
        return True

    @classmethod
    def delete_product(cls, user, product_id):
        product = cls._query_product(charger_id=user.charger_id, product_id=product_id)
        product.delete()
        db.session.commit()
        return True

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
                error_msg='content does not exist',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )
        buyer_id = content['user_id']
        product_id = content['id']
        product = Product.query.filter(
            Product.id == product_id
        ).first()
        if not product:
            raise NotFoundError(
                error_msg='product does not exist',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )
        if product.stock == 0:
            raise ValidationError(
                error_msg='insufficient product stock',
                error_code=ErrorCodes.INSUFFICIENT_PRODUCT_STOCK
            )
        product.stock -= 1
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
