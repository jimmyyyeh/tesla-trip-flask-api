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

from tesla_trip_common.models import AdministrativeDistrict


class AdministrativeDistrictHandler:
    @staticmethod
    def get_administrative_districts():
        administrative_districts = AdministrativeDistrict.query.all()
        results = dict()
        for administrative_district in administrative_districts:
            city = administrative_district.city
            if city not in results:
                results[city] = list()
            result = {
                'id': administrative_district.id,
                'area': administrative_district.area,
            }
            results[city].append(result)
        return results
