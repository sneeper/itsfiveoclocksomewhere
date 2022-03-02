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
from simple_image_download import simple_image_download as simp

stateObj = re.compile('^[A-Za-z][A-Za-z]$')

app = Flask(__name__)
cities = {}

class country:
    def __init__(self, name, languages):
        self.name = name
        self.languages = languages.split(',')

class timezone:
    def __init__(self, timezone, localtime):
        self.timezone = timezone
        self.localtime = localtime

class city:
    def __init__(self, line, countryDict):
        cityinfo = line.split('\t')
        self.name = cityinfo[2]
        country = cityinfo[8]
        if country in countryDict:
            self.country = countryDict[country].name
            self.language = countryDict[country].languages[0]
        maybestate = cityinfo[10]
        self.timezone = cityinfo[17]
        self.state = None
        if stateObj.match(maybestate):
            self.state = maybestate
        if self.state:
            self.fullname = f'{self.name}, {self.state}, {self.country}'
        else:
            self.fullname = f'{self.name}, {self.country}'
    state = None
    country = None
    language = None

def getToast(language):
    salud = None
    general_language = language.split('-')[0] # e.g. en instead of  en-CA
    if language in cheersDict:
        salud = random.choice(cheersDict[language])
    elif general_language in cheersDict:
        salud = random.choice(cheersDict[general_language])
    return salud

def getImageUrl(city):
    items = city.split(',')
    items = [x.strip() for x in items]
    items = [f'"{x}"' for x in items]
    city = " ".join(items)
    #print(city)
    urls = simp.simple_image_download().urls(city, 5)
    #print(urls)
    for x in urls:
        if not "thumb" in x and not "google" in x:
            if x.find('commons.wikimedia.org'):
                x = x.replace('File:', 'Special:FilePath/')
            #print(f'Choosing {x}')
            return x
    return None

def load_country_dict():
    countries = {}
    countryfile = open('countryInfo.txt', 'r')
    for line in countryfile.readlines():
        if line[0] == '#': continue
        country_data = line.split('\t')
        countrycode = country_data[0]
        x = country(name=country_data[4], languages=country_data[15])
        countries[countrycode] = x
    return countries

def load_cities_by_timezone():
    countryDict = load_country_dict()
    cities = {}
    cityfile = open('cities15000.txt', 'r')
    for line in cityfile.readlines():
        x = city(line, countryDict)
       
        if x.timezone in cities:
            cities[x.timezone].append(x)
        else:
            cities[x.timezone] = [x]
    cityfile.close()
    return cities
    
def load_cheers_by_language():
    cheersDict = {}
    for languagefile in os.listdir('cheers'):
        if languagefile[-4:] == '.txt':
            language = languagefile[:-4]
            x = open(f'cheers/{languagefile}', 'r')
            cheerslist = [m.rstrip() for m in x.readlines()]
            x.close()
            cheersDict[language] = cheerslist
    return cheersDict

def get_drinkyzones(drinkytime=17):
    drinkytimezones = []
    all_timezones = pytz.all_timezones
    if 'leapseconds' in all_timezones:
        all_timezones.remove('leapseconds') # why was this in there?!
    for timezonestr in all_timezones:
        tz = pytz.timezone(timezonestr)
        localtime = datetime.now(tz)
        if localtime.hour == drinkytime:
            x = timezone(timezone = timezonestr, localtime = localtime)
            drinkytimezones.append(x)
    return drinkytimezones

def get_drinky_cities(drinktime=17):
    allcities = []
    drinkyzones = get_drinkyzones(drinktime)
    for zone in drinkyzones:
        if zone.timezone in cities.keys():
            for mycity in cities[zone.timezone]:
                mycity.localtime = zone.localtime
                allcities.append(mycity)
    return allcities

def hourStrAMPM(hour):
    x = datetime.now()
    return datetime(year=x.year, month=x.month, day=x.day, hour=hour, minute=x.minute).strftime("%-I %p")

@app.route('/all/<drinktime>')
@app.route('/all')
def allcities(drinktime='17'):
    try:
        dt=int(drinktime)
    except:
        dt=17
    allcities = get_drinky_cities(dt)
    return render_template('all_cities.html', allcities=allcities, dt=hourStrAMPM(dt), cheersDict=cheersDict, getToast=getToast )

@app.route('/<drinktime>')
@app.route('/')
def singlecity(drinktime='17'):
    try:
        dt=int(drinktime)
    except:
        dt=17
    allcities = get_drinky_cities(dt)
    city = random.choice(allcities)
    salud = getToast(city.language)
    #print(salud)
    imgurl = getImageUrl(city.fullname)
    #print(imgurl)
    return render_template('random_city.html', city=escape(city.fullname), localtime=city.localtime, imgurl=imgurl, salud=salud )

cities = load_cities_by_timezone()
cheersDict = load_cheers_by_language()
port = int(os.environ.get('PORT', 80))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)
