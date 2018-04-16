from datetime import datetime

import settings
from datastorage import DataStorage
from graphql.graphql import save_cells, save_current
from radar import collect_rain_data
from radar.utils import DATE_FORMAT
from schiffts_twitter.schiffts_twitter import do_twitter
from weather import get_weather
from radar.hit import handle_new_hit


def save_data(datastorage, rain_at_location, radar_data, next_hit):
    current_timestamp = datetime.strftime(radar_data[0].timestamp, DATE_FORMAT)
    datastorage.save_data(current_timestamp, radar_data, next_hit, rain_at_location)


def save_current_position(data, weather):

    current_data = {
        'intensity': -1
    }

    if data:
        current_data['intensity'] = data['intensity']

    if weather:
        # python min. 3.5
        # current_data = {**current_data, **weather}

        current_data['weatherCode'] = weather['weatherCode']
        current_data['temperature'] = weather['temperature']

    save_current(current_data)


def handle_weather(city):
    weather_at_location = get_weather(city)
    weather_data = None

    if weather_at_location:
        weather_data = {
            'temperature': weather_at_location['current_temp'],
            'weatherCode': weather_at_location['weather_symbol_id']
        }

    return weather_data


def schiffts():

    datastorage = DataStorage("schiffts.json")

    # load old data
    old_data = datastorage.load_data()

    current_rain_at_location, forecast, radar_data = collect_rain_data((settings.X_LOCATION, settings.Y_LOCATION),
                                                                       saved_history=old_data['radar_history'])

    if bool(current_rain_at_location) != bool(old_data['rain_at_position']):
        do_twitter(current_rain_at_location)

    handle_new_hit(forecast)

    weather_data = handle_weather(settings.SMN_CITY_NAME)

    save_data(datastorage, current_rain_at_location, radar_data, forecast['next_hit'])
    save_cells(radar_data[0].cells, False)
    save_current_position(current_rain_at_location, weather_data)

    # todo:
    # get temperature
    # get weather
    # check for snow


if __name__ == '__main__':
    schiffts()
