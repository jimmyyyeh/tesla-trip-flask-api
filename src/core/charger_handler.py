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

from tesla_trip_common.models import SuperCharger


class ChargerHandler:
    @staticmethod
    def get_chargers():
        super_chargers = SuperCharger.query.all()
        results = list()
        for super_charger in super_chargers:
            result = {
                'id': super_charger.id,
                'name': super_charger.name,
                'city': super_charger.city,
                'tpc': super_charger.tpc,
                'ccs2': super_charger.ccs2,
                'floor': super_charger.floor,
                'business_hours': super_charger.business_hours,
                'park_fee': super_charger.park_fee,
                'charger_fee': super_charger.charger_fee,
                'version': super_charger.version
            }
            results.append(result)
        return results
