# python3
'''
cleaned up some duplicate info & requests
Moon info idea from : https://bit.ly/3XRSpox
Wx Data Source : https://www.visualcrossing.com/ (free account, very easy setup)
Wx Icons from VC - https://github.com/visualcrossing/WeatherIcons
    https://github.com/visualcrossing/WeatherIcons/tree/main/PNG/4th%20Set%20-%20Color
~ http://allsky.local/documentation/overlays/overlays.html -> AllSky Fields
'''
import requests
import json
import RPi.GPIO as GPIO
from bs4 import BeautifulSoup # pip install beautifulsoup4
urlWx = 'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/boise%2C%20ID?unitGroup=us&key={{use your own API key}}&contentType=json'
urlKp = 'https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json'
urlKp = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-5-minute.json'
urlBz = 'https://services.swpc.noaa.gov/products/solar-wind/mag-5-minute.json'

weatherFile = '/home/pi/allsky/config/overlay/extra/scrape_wx.json'
img_ext = '.png'

def vcWxScrape():
    pin = 17
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    state = GPIO.input(pin)
    if state:
       heatColor =  "#f56b6b" #"#ff0000" #red'ish
       heaterStat = "Heater = ON"
    else:
       heatColor = "#009900" #green
       heaterStat = "Heater = Off"
    try:
        with requests.get(urlWx) as wxFile:
            soupWx = BeautifulSoup(wxFile.content, 'html.parser')
            wxData = json.loads(str(soupWx))
            wxVals = (wxData['currentConditions'])
            tmpWx = wxVals['temp']              # Temperature
            feelsWx = wxVals['feelslike']       # Temperature Feels-Like
            dewWx = wxVals['dew']               # Dewpoint
            humWx = wxVals['humidity']          # Humidity
            windWx = wxVals['windspeed']        # WindSpeed
            presWx = wxVals['pressure']         # Pressure
            sRiseWx = wxVals['sunrise']         # Sunrise
            sSetWx = wxVals['sunset']           # Sunset
            moonWx = wxVals['moonphase']        # Moon Phase
            moonWx = round(moonWx, 2)           # Moon Phase - Rounded
            condWx = wxVals['conditions']       # Conditions
            #desWx = wxVals['description']      # Description
            iconWx = wxVals['icon']             # Weather Icon - maybe no.
            iconWxIc = (iconWx + img_ext)
    except json.decoder.JSONDecodeError:
        pass
    try:
        if moonWx == 0:
            moonPhsWx = "New Moon"
            moonWx = moonWx * 200
        elif moonWx >0 and moonWx <0.25:
            moonPhsWx = "Waxing Crescent"
            moonWx = moonWx * 200
        elif moonWx == 0.25:
            moonPhsWx = "First Quarter"
            moonWx = moonWx * 200
        elif moonWx >0.25 and moonWx <0.5:
            moonPhsWx = "Waxing Gibbous"
            moonWx = moonWx * 200
        elif moonWx == 0.5:
            moonPhsWx = "Full Moon"
            moonWx = 100
        elif moonWx >0.5 and moonWx <0.75:
            moonPhsWx = "Waining Gibbous"
            moonWx = (1 - moonWx) * 200
        elif moonWx == 0.75:
            moonPhsWx = "Last Quarter"
            moonWx = (1 - moonWx) * 200
        elif moonWx >0.75 and moonWx <=1:
            moonPhsWx = "Waining Gibbous"
            moonWx = (1 - moonWx) * 200
        dictionary = {
            "VC_TMP":{
            "value":tmpWx,
            "expires":0,
            },
            "VC_FEELS":{
            "value":feelsWx,
            "expires":0,
            },
            "VC_DEW":{
            "value":dewWx,
            "expires":0,
            },
            "VC_HUM":{
            "value":humWx,
            "expires":0,
            },
            "VC_WIND":{
            "value":windWx,
            "expires":0,
            },
            "VC_PRES":{
            "value":presWx,
            "expires":0,
            },
            "VC_SRISE":{
            "value":sRiseWx,
            "expires":0,
            },
            "VC_SSET":{
            "value":sSetWx,
            "expires":0,
            },
            "VC_MOON":{
            "value":round(moonWx,2), #round to prevent excessive length
            "expires":0,
            },
            "VC_MOONPHS":{
            "value":moonPhsWx,
            "expires":0,
            },
            "VC_COND":{
            "value":condWx,
            "expires":0,
            },
            "VC_ICON":{
            #"value":iconWx,
            "image":iconWxIc,
            "x": 160,
            "y": 1345, #1765 for bottom location
            "scale": 2,
            "expires": 6000,
            "opacity": 1
            },
            "HEATER_STAT":{
            "value":heaterStat,
            "fill":heatColor,
            "expires":0,
            },
            # "CLEARSKY_IMG":{
            # #"value":clearskyimg,
            # "image":"/home/pi/jscripts/tmp/BoiseIDcs0.jpg",
            # "x": 745,
            # "y": 2010, #1765 for bottom location
            # "scale": 3,
            # "expires": 6000,
            # "opacity": 1
            # },
        }
        # Writing to temp_json file
        json_object = json.dumps(dictionary, indent=4)
        with open(weatherFile, "w") as outfile:
            outfile.write(json_object)
    except json.decoder.JSONDecodeError:
        pass

vcWxScrape()
GPIO.cleanup()
