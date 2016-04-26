# -*- coding: utf-8 -*-

import os
import json
import requests
from datetime import datetime
from os import path
from bottle import route, run, template, request

def render_template(template_name, **kwargs):
    filename = path.join(path.dirname(path.abspath(__file__)), 'templates', template_name)
    with open(filename, 'r') as t:
        return template(t.read(), **kwargs)

@route('/')
def index():
    return render_template('index.html')

@route('/api/openweathermap/')
def openweathermap():
    city = request.query.city or 'Saint Petersburg'
    country = request.query.country or 'Russia'
    apikey = os.getenv('OPENWEATHERMAP_APIKEY')

    url = 'http://api.openweathermap.org/data/2.5/weather?APPID={}&q={},{}'.format(apikey, city, country)
    resp = requests.get(url)

    if resp.status_code != 200:
        return 'Error: code={}, reason={}'.format(resp.status_code, resp.reason)

    return resp.json()


@route('/api/openweathermap_5_days/')
def openweathermap_5_days():
    city = request.query.city or 'Saint Petersburg'
    country = request.query.country or 'Russia'
    apikey = os.getenv('OPENWEATHERMAP_APIKEY')

    url = 'http://api.openweathermap.org/data/2.5/forecast?APPID={}&q={},{}'.format(apikey, city, country)
    resp = requests.get(url)

    if resp.status_code != 200:
        return 'Error: code={}, reason={}'.format(resp.status_code, resp.reason)

    return resp.json()


@route('/api/yahoo/')
def yahoo():
    city = request.query.city or 'Saint Petersburg'
    country = request.query.country or 'Russia'

    url = "https://query.yahooapis.com/v1/public/yql?{}&format=json"
    params = {
        'q': ('select * from weather.forecast where woeid in '
              '(select woeid from geo.places(1) where text="{},{}")'.format(city, country)),
        'format': 'json'
    }

    resp = requests.get(url, params=params)
    if resp.status_code != 200:
        return 'Error: code={}, reason={}'.format(resp.status_code, resp.reason)

    return resp.json()

run(host='localhost', port=8080, reloader=True)
