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

import os


class Config:
    ENVIRONMENT = os.environ.get('ENVIRONMENT', 'develop')
    API_DOMAIN = os.environ['API_DOMAIN']
    WEB_DOMAIN = os.environ['WEB_DOMAIN']

    # mysql
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['MYSQL_USER']
    DB_PWD = os.environ['MYSQL_PASSWORD']
    DB_HOST = os.environ['MYSQL_HOST']
    DB_PORT = os.environ['MYSQL_PORT']

    # redis
    REDIS_HOST = os.environ['REDIS_HOST']
    REDIS_PASSWORD = os.environ.get('REDIS_PASSWORD', None)
    REDIS_PORT = os.environ['REDIS_PORT']

    SQLALCHEMY_BINDS = {
        DB_NAME: f'mysql+pymysql://{DB_USER}:{DB_PWD}@{DB_HOST}:{DB_PORT}/{DB_NAME}',
    }
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_AS_ASCII = False

    # JWT
    ACCESS_TOKEN_EXPIRE_TIME = 60 * 5
    REFRESH_TOKEN_EXPIRE_TIME = 60 * 60 * 24  # 一天
    SALT = os.environ['SALT']

    # mail

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_MAX_EMAILS = 10
    MAIL_USERNAME = os.environ['MAIL_USERNAME']
    MAIL_PASSWORD = os.environ['MAIL_PASSWORD']
    MAIL_DEFAULT_SENDER = ('Tesla Trip', MAIL_USERNAME)
