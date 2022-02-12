#!/usr/bin/python3
#
# countryInfo from http://download.geonames.org/export/dump/
# cities15000.txt from http://download.geonames.org/export/dump/
# 
#
#
import pytz
import random
import re
import os
from datetime import datetime
from flask import Flask, render_template
from markupsafe import escape

stateObj = re.compile('^[A-Za-z][A-Za-z]$')

app = Flask(__name__)
cities = {}


def load_country_dict():
    countries = {}
    countryfile = open('countryInfo.txt', 'r')
    for line in countryfile.readlines():
        if line[0] == '#': continue
        country_data = line.split('\t')
        countrycode = country_data[0]
        countryname = country_data[4]
        countries[countrycode] = countryname
    return countries

def load_cities_by_timezone():
    countries = load_country_dict()
    cities = {}
    cityfile = open('cities15000.txt', 'r')
    for line in cityfile.readlines():
        cityinfo = line.split('\t')
        cityname = cityinfo[2]
        country = cityinfo[8]
        maybestate = cityinfo[10]
        state=None 
        if stateObj.match(maybestate):
            state = maybestate

        if country in countries:
            country = countries[country]
       
        if state:
            fullname = f'{cityname}, {state}, {country}'
        else:
            fullname = f'{cityname}, {country}'
        timezone = cityinfo[17]
       
        if timezone in cities:
            cities[timezone].append(fullname)
        else:
            cities[timezone] = [fullname]
    cityfile.close()
    return cities
    

def get_drinkyzones(drinkytime=17):
    drinkytimezones = []
    all_timezones = pytz.all_timezones
    if 'leapseconds' in all_timezones:
        all_timezones.remove('leapseconds') # why was this in there?!
    for timezone in all_timezones:
        tz = pytz.timezone(timezone)
        localtime = datetime.now(tz)
        if localtime.hour == drinkytime:
            drinkytimezones.append(timezone)
    return drinkytimezones

def get_drinky_cities(drinktime=17):
    allcities = []
    drinkyzones = get_drinkyzones(drinktime)
    for zone in drinkyzones:
        if zone in cities:
            for city in cities[zone]:
                allcities.append(city)
    return allcities

def hourStr(hour):
    x = datetime.now()
    return datetime(year=x.year, month=x.month, day=x.day, hour=hour).strftime("%-I")

def hourStrAMPM(hour):
    x = datetime.now()
    return datetime(year=x.year, month=x.month, day=x.day, hour=hour).strftime("%-I %p")

@app.route('/all/<drinktime>')
@app.route('/all')
def allcities(drinktime='17'):
    try:
        dt=int(drinktime)
    except:
        dt=17
    allcities = get_drinky_cities(dt)
    return render_template('all_cities.html', allcities=allcities, dt=hourStrAMPM(dt))

@app.route('/<drinktime>')
@app.route('/')
def singlecity(drinktime='17'):
    try:
        dt=int(drinktime)
    except:
        dt=17
    allcities = get_drinky_cities(dt)
    city = random.choice(allcities)
    return render_template('random_city.html', city=escape(city), dtampm=hourStrAMPM(dt), dt=hourStr(dt))

cities = load_cities_by_timezone()
port = int(os.environ.get('PORT', 80))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
