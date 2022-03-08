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

import redis

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_compress import Compress
from flask_cors import CORS
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config.Config')
config = app.config

CORS(app, send_wildcard=True)  # 允許跨域請求
Compress(app)  # 壓縮

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
mail = Mail(app)

redis_instance = redis.StrictRedis(
    host=config['REDIS_HOST'],
    password=config['REDIS_PASSWORD'],
    port=config['REDIS_PORT'],
    charset='utf-8',
    decode_responses=True,
)


def create_app():
    return app
