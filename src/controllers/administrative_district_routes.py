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
from core.administrative_district_handler import AdministrativeDistrictHandler
from utils.auth_tool import AuthTool
from utils.response_handler import ResponseHandler


@app.route('/administrative-district', methods=['GET'])
@AuthTool.sign_in()
def get_administrative_district(user):
    result = AdministrativeDistrictHandler.get_administrative_districts()
    return ResponseHandler.package_result(result=result)
