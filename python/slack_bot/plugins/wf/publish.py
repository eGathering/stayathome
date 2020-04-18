#!/usr/bin/python3
"""
REST APIでサーバーに問い合わせを行うモジュール
"""

import requests
import json

from .location import Location

def _create_params(name):
    location = Location()
    id = location.findId(name)
    if id:
        return {'city': id}
    return None

def request(name):
    apiurl = 'http://weather.livedoor.com/forecast/webservice/json/v1'
    response = requests.get(apiurl, _create_params(name))
    if response:
        return json.loads(response.content)['forecasts']
    return None

