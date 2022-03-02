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

from flask import jsonify
from loguru import logger
from schema import SchemaError

from app import app
from utils.error_codes import ErrorCodes


def make_error_schema(error_code, error_msg):
    _dict = {
        'error_code': error_code,
        'error_msg': error_msg
    }
    logger.exception(error_msg)
    return _dict


class _BaseError(Exception):
    """
        base error class
    """

    def __init__(self, code=404, error_msg=None, error_code=None):
        super(_BaseError, self).__init__()
        self.code = code
        self.error_code = error_code
        self.error_msg = error_msg

    def __str__(self):
        return self.__class__.__name__

    def to_dict(self):
        return make_error_schema(
            error_msg=self.error_msg, error_code=self.error_code)


class ValidationError(_BaseError):
    def __init__(self, error_msg=None, error_code=None):
        super(ValidationError, self).__init__(
            code=400, error_msg=error_msg, error_code=error_code
        )


class NotFoundError(_BaseError):
    def __init__(self, error_msg=None, error_code=None):
        super(NotFoundError, self).__init__(
            code=404, error_msg=error_msg, error_code=error_code
        )


@app.errorhandler(ValidationError)
def handle_validation_error(e):
    return jsonify(e.to_dict()), e.code


@app.errorhandler(NotFoundError)
def handle_not_found_error(e):
    return jsonify(e.to_dict()), e.code


@app.errorhandler(Exception)
def handle_500_error(e):
    return jsonify(make_error_schema(error_code=ErrorCodes.BASE_ERROR, error_msg=str(e))), 500


@app.errorhandler(SchemaError)
def handle_schema_error(e):
    return jsonify(make_error_schema(error_code=ErrorCodes.PAYLOAD_ERROR, error_msg=str(e))), 422
