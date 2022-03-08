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

    USER_NOT_EXISTS = 1001  # 使用者不存在
    USER_INVALIDATE = 1002  # 使用者授權無效(密碼錯誤)
    USER_ALREADY_EXISTS = 1003   # 使用者已存在
    INVALID_TOKEN = 1004  # 無效授權
    TOKEN_EXPIRED = 1005  # 授權逾時
    TOKEN_MISSING = 1006  # headers 未帶授權
    VERIFY_TOKEN_NOT_FOUND = 1007  # 驗證資訊不在

    PAYLOAD_ERROR = 2001  # 參數錯誤
    DATA_NOT_EXIST = 2022  # 資料不存在
