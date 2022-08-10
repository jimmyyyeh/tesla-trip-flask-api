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

from core.administrative_district_handler import AdministrativeDistrictHandler
from utils.auth_tool import AuthTool
from utils.response_handler import ResponseHandler

administrative_district_app = Blueprint('administrative_district', __name__)


@administrative_district_app.route('/', methods=['GET'])
@swag_from('../swagger_yaml/administrative_district/get_administrative_district.yaml')
@AuthTool.sign_in()
def get_administrative_district(user):
    result = AdministrativeDistrictHandler.get_administrative_districts()
    return ResponseHandler.package_result(result=result)
