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

from flask import send_file
from os import path
from app import config
from utils.errors import NotFoundError
from utils.error_codes import ErrorCodes


class ImageHandler:
    @staticmethod
    def _return_image(file_path):
        if path.exists(file_path):
            return send_file(file_path)
        else:
            raise NotFoundError(
                error_msg='image does not exists',
                error_code=ErrorCodes.DATA_NOT_EXISTS
            )

    @classmethod
    def get_image(cls, filename):
        file_path = f'{config["STATIC_PATH"]}{filename}'
        results = cls._return_image(file_path=file_path)
        return results
