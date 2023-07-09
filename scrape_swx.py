#!/usr/lib/python3

import ephem
import pytz
import datetime
import requests
import json
from bs4 import BeautifulSoup  # pip install beautifulsoup4

swxFile = '/home/pi/allsky/config/overlay/extra/scrape_swx.json'
urlKp = 'https://services.swpc.noaa.gov/products/noaa-planetary-k-index.json'
urlWind = 'https://services.swpc.noaa.gov/products/solar-wind/plasma-6-hour.json'
urlBz = 'https://services.swpc.noaa.gov/products/solar-wind/mag-6-hour.json'

utcnow = datetime.datetime.now(tz=pytz.UTC)
dtUtc = utcnow.replace(microsecond=0, tzinfo=None)
UTCformat = dtUtc.strftime("%Y-%m-%d %H:%M:%S")

obs = ephem.Observer()
obs.lat = '43:32'    # Use your own Latitude
obs.long = '-116:18'  # Use your own Longitude
obs.date = UTCformat

sun = ephem.Sun(obs)
sun.compute(obs)
sun_angle = round(float(sun.alt) * 57.2957795, 1)

def get_color(value, ranges, colors):
    for i in range(len(ranges) - 1):
        if ranges[i] <= value < ranges[i+1]:
            return colors[i]
    return colors[-1]

def swxScrape():
    try:
        with requests.get(urlWind) as rWind:
            soupWind = BeautifulSoup(rWind.content, 'html.parser')
            dataWind = json.loads(str(soupWind))
            densityData = dataWind[len(dataWind)-1][1]
            speedData = dataWind[len(dataWind)-1][2]
            tempData = dataWind[len(dataWind)-1][3]

            if densityData is not None:
                densityData = float(densityData)
                densityColor = ''  # Default value
                if densityData > 6:
                  densityColor = "#10e310" #green
                elif densityData >= 2 and densityData <= 6:
                 densityColor = "#ffec00" #yellow'ish
                elif densityData < 2:
                  densityColor = "#f56b6b" #red'ish
                else:
                  densityColor="#10e310" #gray
            if speedData is not None:
                speedData = float(speedData)
                speedColor = ''  # Default value
                if speedData < 500:
                  speedColor = "#10e310" #green
                elif speedData >= 500 and speedData <= 550:
                  speedColor = "#ffec00" #yellow'ish
                elif speedData > 550:
                  speedColor = "#f56b6b" #red'ish
                else:
                  speedColor="#10e310" #gray
            if tempData is not None:
                tempData = float(tempData)
                tempDataFmt = format(tempData, ',').rstrip('0').rstrip('.')
                tempColor = ''  # Default value
                if tempData >= 500001:
                    tempColor = "#f56b6b" #red'ish
                elif tempData >= 300001:
                    tempColor = "#ffec00" #yellow'ish
                elif tempData >= 100001:
                    tempColor = "#10e310" #green
                elif tempData >= 50000:
                    tempColor = "#ffec00" #yellow'ish
                else:
                    tempColor = "#f56b6b" #red'ish
            else:
                tempDataFmt = ''  # Assign an appropriate default value
                tempColor = ''    # Assign an appropriate default value

    except json.decoder.JSONDecodeError:
        pass

    try:
        with requests.get(urlKp) as rKp:
            soupKp = BeautifulSoup(rKp.content, 'html.parser')
            dataKp = json.loads(str(soupKp))
            kpData = dataKp[len(dataKp)-1][1]
            if kpData is not None:
                kpData = float(kpData)
                if kpData < 4:
                    kpColor = "#10e310" #green
                elif kpData >= 4 and kpData <= 5:
                    kpColor = "#ffec00" #yellow'ish
                elif kpData > 5:
                    kpColor = "#f56b6b" #red'ish
                else:
                    kpColor = "#10e310" #gray
            else:
                kpData = 0.0  # Assign an appropriate default value
                kpColor = ''  # Assign an appropriate default value

    except json.decoder.JSONDecodeError:
        pass

    try:
        with requests.get(urlBz) as rBz:
            soupBz = BeautifulSoup(rBz.content, 'html.parser')
            dataBz = json.loads(str(soupBz))
            bzData = dataBz[len(dataBz)-1][3]
            if bzData is not None:
                bzData = float(bzData)
                if bzData > -6:
                    bzColor = "#10e310" #green
                elif bzData <= -6 and bzData > -15:
                    bzColor = "#ffec00" #yellow'ish
                elif bzData <= -15:
                    bzColor = "#f56b6b" #red'ish
                else:
                    bzColor = "#808080" #gray
            else:
                bzData = 0.0  # Assign an appropriate default value
                bzColor = ''  # Assign an appropriate default value

    except json.decoder.JSONDecodeError:
        pass

    try:
        dictionary = {
            "SWX_SWIND_SPEED": {
                "value": speedData,
                "fill": speedColor,
                "expires": 0,
            },
            "SWX_SWIND_DENSITY": {
                "value": densityData,
                "fill": densityColor,
                "expires": 0,
            },
            "SWX_SWIND_TEMP": {
                "value": tempDataFmt,
                "fill": tempColor,
                "expires": 0,
            },
            "SWX_KPDATA": {
                "value": kpData,
                "fill": kpColor,
                "expires": 0,
            },
            "SWX_BZDATA": {
                "value": bzData,
                "fill": bzColor,
                "expires": 0,
            },
            "SWX_S_ANGLE": {
                "value": sun_angle,
                "expires": 0,
            },
        }

        json_object = json.dumps(dictionary, indent=4)
        with open(swxFile, "w") as outfile:
            outfile.write(json_object)

    except json.decoder.JSONDecodeError:
        pass


swxScrape()
