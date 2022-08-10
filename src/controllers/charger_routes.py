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
from flasgger import swag_from

from core.charger_handler import ChargerHandler
from utils.auth_tool import AuthTool
from utils.response_handler import ResponseHandler

super_charger_app = Blueprint('super_charger', __name__)


@super_charger_app.route('/', methods=['GET'])
@swag_from('../swagger_yaml/super_charger/get_super_charger.yaml')
@AuthTool.sign_in()
def get_super_charger(user):
    result = ChargerHandler.get_chargers()
    return ResponseHandler.package_result(result=result)
