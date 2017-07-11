import settings
from datetime import datetime

from graphql.graphql import save_cells, save_current
from radar import get_rain
from radar.forecast import find_cell_index_in_history
from radar.utils import DATE_FORMAT
from datastorage import DataStorage
from schiffts_twitter.schiffts_twitter import do_twitter, tweet_prediction


def save_data(datastorage, rain_at_location, radar_data, next_hit):
    current_timestamp = datetime.strftime(radar_data[0].timestamp, DATE_FORMAT)
    datastorage.save_data(current_timestamp, radar_data, next_hit, rain_at_location)


def handle_new_hit(forecast, old_hit):

    if not forecast['next_hit']:
        return

    if not old_hit or not find_cell_index_in_history(forecast['hit_history'], old_hit):
        tweet_prediction(forecast['next_hit'])


def save_current_position(data):

    intensity = -1

    if data:
        intensity = data['intensity']

    save_current(intensity)


def schiffts():

    datastorage = DataStorage("schiffts.json")

    # load old data
    old_data = datastorage.load_data()

    current_rain_at_location, forecast, radar_data = get_rain((settings.X_LOCATION, settings.Y_LOCATION),
                                                              old_history=old_data['radar_history'])

    if bool(current_rain_at_location) != bool(old_data['rain_at_position']):
        do_twitter(current_rain_at_location)

    handle_new_hit(forecast, old_data['next_hit'])

    save_data(datastorage, current_rain_at_location, radar_data, forecast['next_hit'])
    save_cells(radar_data[0].cells, False)
    save_current_position(current_rain_at_location)

    # todo:
    # get temperature
    # get weather
    # check for snow

if __name__ == '__main__':
    schiffts()
