# export FLASK_ENV=development
import os
import pprint
import datetime
import random

from flask import Flask, request, render_template

app = Flask(__name__) 

cityDict = {}

# https://www.timeanddate.com/time/map/
def getUTCOffset():
    utc_now = datetime.datetime.utcnow()
    offset = 17 - utc_now.hour
    if offset > 12:
        offset = -(offset - 12)   # does this logic work?
    return offset

def loadCities():
    for cityfile in os.listdir("cities"):
        offset = cityfile.strip(".txt")
        cityDict[offset] = []
        cityhandle = open("cities/" + cityfile, "r")
        for line in cityhandle.readlines():
            cityDict[offset].append(line.strip())
        cityhandle.close()
        
@app.route('/utcoffset')
def utcoffset():  # temporary
    offset = getUTCOffset()
    index = "UTC+%d_00" % offset
    output = "offset = %d .  index = %s" % (offset, index)
    return output
    
@app.route('/')
def index():
    loadCities()
    #cities = pprint.pformat(cityDict)
    offset = getUTCOffset()
    index = "UTC+%d_00" % offset
    if index in cityDict:
        citylist = cityDict[index]
    mycity = random.choice(citylist)
    return render_template("index.html", city = mycity)

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 5000)) 
	app.run(host='0.0.0.0', port=port)  #Start listening
