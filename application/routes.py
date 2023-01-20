import os

import requests
from flask import Blueprint, request, make_response, render_template, redirect, url_for
import datetime
import json
from application.models import User, Location


API_KEY_WEATHER = os.environ['API_KEY_WEATHER']
page = Blueprint('page', __name__, template_folder='templates')


def find_city_coordinates_by_api(city):
    url = 'http://api.openweathermap.org/geo/1.0/direct?q={}&limit=5&appid={}'.format(city, API_KEY_WEATHER)
    return requests.get(url).json()[0]


def save_new_city_in_location_table(city):
    coords = find_city_coordinates_by_api(city)
    new_city = Location(
        city=city.lower(),
        latitude=coords['lat'],
        longitude=coords['lon'])
    new_city.save()
    return new_city


@page.route('/coordinates/<city_>')
def print_coordinates(city_):
    existing_city = Location.query.filter(Location.city == city_.lower()).first()
    if existing_city:
        if not existing_city.latitude and not existing_city.longitude:
            coords = find_city_coordinates_by_api(existing_city.city)
            existing_city.latitude = coords['lat']
            existing_city.longitude = coords['lon']
            existing_city.save()
        city_=existing_city
    else:
        city_ = save_new_city_in_location_table(city_)
    return make_response(
        f'City {city_.city} with coordinates latitude= {city_.latitude} and longitude= {city_.longitude}'
    )


@page.route('/coordinates', methods=['GET', 'POST'])
def get_city_coords():
    """Create a user via query string parameters."""
    if request.method == 'GET':
        return render_template('get_city_coords.html')
    else:
        city_ = request.form['city']
        return redirect(url_for('page.print_coordinates', city_=city_))


def get_weather_today(city):
    url = 'https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&units=metric&appid={}'.format(
        city.latitude, city.longitude, API_KEY_WEATHER)
    return requests.get(url).json()['main']



@page.route('/weather/<city_>')
def print_weather_by_city(city_):
    existing_city = Location.query.filter(Location.city == city_.lower()).first()
    location = existing_city if existing_city else save_new_city_in_location_table(city_)
    return make_response(
        f'Weather in city {location.city} is {get_weather_today(location)}'
    )


@page.route('/weather', methods=['GET', 'POST'])
def get_weather_by_city():
    if request.method == 'GET':
        return render_template('get_weather.html')
    else:
        city_name = request.form['city']
        return redirect(url_for('page.print_weather_by_city', city_=city_name))


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


@page.route('/success/<name>')
def success(name):
    return 'welcome %s' % name


@page.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        user = request.form['nm']
        return redirect(url_for('page.success', name=user))
    else:
        return render_template("login.html")