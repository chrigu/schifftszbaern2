# -*- coding: utf-8 -*-
import requests
from lxml import html

DOMAIN = "www.meteoswiss.admin.ch"

"""
Weather Symbols
---------------

1 = sunny
101 = clear sky
2 = mostly sunny, some clouds
102 = mostly clear sky, some clouds
35 = overcast and dry
3 = partly sunny, thick passing clouds
4 = overcast
14 = very cloudy, light rain
5 = very cloudy
21 = very overcast with frequent sleet
6 = sunny intervals,  isolated showers
15 = very cloudy, light sleet
16 = very cloudy, light snow
17 = very cloudy, rain
18 = very cloudy, rain & snow
19 = very cloudy, snow
20 = very overcast with rain
22 = very overcast with heavy snow
23, 24 = thunderstomrs
25 = thunderstomrs & heavy rain
29 = Sunny intervals, scattered showers
7, 10 = sunny intervals, showers & snow, sleet
8, 11 = sunny intervals,  snow showers
9 = sunny intervals, showers
12 = cloudy with thunder (light & sun)
13 = cloudy with thunder (sun, rain)
26 = sunny with high clouds
27 = fog sunny above
28 = foggy
30 = light clouds some snow, partly sunny
31 = light clouds some snow & rain, partly sunny
32 = light clouds some rain, partly sunny
33 = clouds rain, partly sunny
34 = clouds some snow, partly sunny

"""


def get_weather(location_code):

    # get page
    page = requests.get("http://{}/home/weather/measurement-values/current-weather.html".format(DOMAIN))
    tree = html.fromstring(page.text)

    # get url for json
    map_div = tree.xpath("//div[@id='current-weather-map']/@data-json-url")

    if len(map_div) > 0:

        data_response = requests.get('http://{}{}'.format(DOMAIN, map_div[0]))
        if data_response.status_code == 200:
            for location in data_response.json()['data']:

                if location['name'] == location_code:
                    berne_data = location
                    return berne_data

    return None

