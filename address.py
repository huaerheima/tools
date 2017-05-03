# -*- coding: utf-8 -*-

import json
import requests

from exception import AddressException


class Address(object):

    def __init__(self, address=None, location=None):
        self._address = address
        self._location = location
        self._component = None
        self._base_url = "http://api.map.baidu.com"
        self._params = {'output': 'json', 'ak': 'GRlG8i8IeHcupO8GR77s5LHGPk27kBlT'}

    @property
    def address(self):
        return self._get_address()

    @property
    def location(self):
        return self._location if self._location else self._get_location()

    @property
    def province(self):
        self._set_address()
        return self._component['province']

    @property
    def city(self):
        self._set_address()
        return self._component['city']

    @property
    def district(self):
        self._set_address()
        return self._component['district']

    def route(self, address):
        return self._get_route_info(address)

    def _set_address(self):
        if not self._component:
            self._address = self._get_address()

    def _get_route_info(self, address):
        func_url = '/routematrix/v2/driving'
        origin = ','.join(map(str, self.location))
        destination = ','.join(map(str, address.location))
        params = self._params.copy()
        params.update(origins=origin, destinations=destination)

        result = requests.get(self._base_url + func_url, params=params)
        data = json.loads(result.text)
        if data['status'] == 0:
            return data['result'][0]['duration']['value'], data['result'][0]['distance']['value']
        else:
            raise AddressException(40000)

    def _get_location(self):
        func_url = '/geocoder/v2/'
        params = self._params.copy()
        params.update(address=self._address)

        result = requests.get(self._base_url + func_url, params)
        data = json.loads(result.text)
        if data['status'] == 0:
            return data['result']['location']['lat'], data['result']['location']['lng'],
        else:
            raise AddressException(40001)

    def _get_address(self):
        if not self._component:
            func_url = '/geocoder/v2/'
            params = self._params.copy()
            params.update(location=",".join(map(str, self.location)))

            result = requests.get(self._base_url + func_url, params)
            data = json.loads(result.text)
            if data['status'] == 0:
                if data['result']['formatted_address']:
                    self._component = data['result']['addressComponent']
                    self._address = data['result']['formatted_address'] + data['result']['sematic_description']
                    return self._address
                else:
                    raise AddressException(40001)
            else:
                raise AddressException(40000)


if __name__ == "__main__":
    # example

    point_1 = Address(address="金隅嘉华大厦")
    print(point_1.address)
    print(point_1.location)
    print(point_1.province)
    print(point_1.city)
    print(point_1.district)
    print()

    point_2 = Address(location=(40.07871264866282, 116.33392797379916))
    print(point_2.address)
    print(point_2.location)
    print(point_2.province)
    print(point_2.city)
    print(point_2.district)
    print()

    # print(point_2.route(point_1))
    # print(Address.route(point_2, point_1))
