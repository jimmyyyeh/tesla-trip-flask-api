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


class ErrorCodes:
    BASE_ERROR = 500

    USER_NOT_EXIST = 1001  # 使用者不存在
    USER_INVALIDATE = 1002  # 使用者授權無效(密碼錯誤)
    INVALID_TOKEN = 1003  # 無效授權
    TOKEN_EXPIRED = 1004  # 授權逾時
    token_missing = 1005  # headers 未帶授權

    PAYLOAD_ERROR = 2001  # 參數錯誤
    DATA_NOT_EXIST = 2022  # 資料不存在
