import os

import requests
from flask import Blueprint, request, make_response, render_template
import datetime
import json
from application.models import User, Location


API_KEY_WEATHER = os.environ['API_KEY_WEATHER']
page = Blueprint('page', __name__, template_folder='templates')


def get_city_coordinates(city):
    url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}'.format(city, API_KEY_WEATHER)
    return requests.get(url).json()[0]


def save_new_city_in_location_table(city):
    coords = get_city_coordinates(city)
    new_city = Location(
        city=city.lower(),
        latitude=coords['lat'],
        longitude=coords['lon'])
    new_city.save()
    return new_city


@page.route('/<city_>', methods=['GET', 'POST'])
def save_city_coords(city_):
    """Create a user via query string parameters."""

    existing_city = Location.query.filter(Location.city == city_.lower()).first()
    if existing_city:
        if existing_city.latitude and existing_city.longitude:
             return make_response(
                f'City {existing_city.city} with coordinates latitude= ({existing_city.latitude}) and longitude= ({existing_city.longitude}) already exists!'
            )

        coords = get_city_coordinates(existing_city.city)
        existing_city.latitude = coords['lat']
        existing_city.longitude = coords['lon']
        existing_city.save()
        return make_response(
            f'Latitude= ({existing_city.latitude}) and longitude= ({existing_city.longitude}) for city {existing_city.city} were just saved!'
        )

    new_city = save_new_city_in_location_table(city_)
    return make_response(
        f'New city {new_city.city} with coordinates latitude= ({new_city.latitude}) and longitude= ({new_city.longitude}) was just created!'
    )


def get_weather_today(city):
    url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}'.format(
        city.latitude, city.longitude, API_KEY_WEATHER)

    return requests.get(url).json()['main']


@page.route('/weather/<city_>', methods=['GET', 'POST'])
def get_weather_by_city(city_):
    existing_city = Location.query.filter(Location.city == city_.lower()).first()
    location = existing_city if existing_city else save_new_city_in_location_table(city_)
    return make_response(
        f'Weather in city {location.city} is {get_weather_today(location)}'
    )


def possible_earthquakes_data_format(earthquakes):
    possible_earthquakes = {}
    num=1
    for earthquake in earthquakes:
        data = earthquake['properties']
        possible_earthquakes[num] = {
            'place': data['place'],
            'magnitude': data['mag'],
            'day': datetime.datetime.fromtimestamp(data['time'] / 1000.0).isoformat()[:10],
            'url': data['url'],
            'tsunami': data['tsunami'],
            'type': data['type']
        }
        num +=1
    return possible_earthquakes


@page.route('/earthquakes/<city_>', methods=['GET'])
def get_earthquakes(city_):
    existing_city = Location.query.filter(Location.city == city_.lower()).first()
    if existing_city:
        day_today = datetime.date.today()
        base_url = 'https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&'
        earthquake_url = base_url + f'starttime={day_today}&endtime={day_today + datetime.timedelta(days=6)}& \
                                    lat={existing_city.latitude}&lon={existing_city.longitude}&maxradiuskm=2000'

        earthquakes = requests.get(earthquake_url).json()['features']
        if earthquakes:
            return make_response(
                f'For city {existing_city.city} possible earthquakes in max radius 2000km are : '
                f'{possible_earthquakes_data_format(earthquakes)}')
        return make_response(
            f'For city {existing_city.city} there are no possible earthquakes in max radius 2000km')
    return get_earthquakes(save_new_city_in_location_table(city_).city)
