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

from app import redis_instance


class RedisKey:
    @staticmethod
    def verify_token(verify_token):
        return f'verify_token:{verify_token}'


class RedisHandler:
    @staticmethod
    def set_verify_token(verify_token, id_):
        key = RedisKey.verify_token(
            verify_token=verify_token
        )
        redis_instance.set(key, value=id_, ex=60 * 5)

    @staticmethod
    def get_verify_token(verify_token):
        key = RedisKey.verify_token(
            verify_token=verify_token
        )
        value = redis_instance.get(key)
        return value
