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

bind = '0.0.0.0:5000'
workers = 1
errorlog = '-'
loglevel = 'info'
accesslog = '-'
access_log_format = '[%({x-real-ip}i)s] %(t)s "%(r)s" %(s)s "%(f)s" "%(a)s"'
# [IP / time / status line / status / refer / user agent]
worker_class = 'gevent'
