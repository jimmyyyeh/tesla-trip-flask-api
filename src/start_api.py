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

from app import create_app, config
from controllers import administrative_district_app, car_app, super_charger_app, image_app, product_app, qrcode_app, \
    trip_app, user_app

app = create_app()

env = config['ENVIRONMENT']
debug = env == 'develop'

app.register_blueprint(administrative_district_app, url_prefix='/administrative-district')
app.register_blueprint(car_app, url_prefix='/car')
app.register_blueprint(super_charger_app, url_prefix='/super-charger')
app.register_blueprint(image_app, url_prefix='/image')
app.register_blueprint(product_app, url_prefix='/product')
app.register_blueprint(qrcode_app, url_prefix='/qrcode')
app.register_blueprint(trip_app, url_prefix='/trip')
app.register_blueprint(user_app)

if __name__ == '__main__':
    app.run(debug=debug, host='0.0.0.0', port=5000)
