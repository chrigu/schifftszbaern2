import settings
from datetime import datetime

from graphql.graphql import save_cells
from radar import get_rain
from radar.forecast import find_cell_index_in_history
from radar.utils import DATE_FORMAT
from datastorage import DataStorage
from schiffts_twitter.schiffts_twitter import do_twitter, tweet_prediction


def save_data(datastorage, rain_at_location, radar_data, next_hit):
    current_timestamp = datetime.strftime(radar_data[0].timestamp, DATE_FORMAT)
    datastorage.save_data(current_timestamp, radar_data, next_hit, rain_at_location)


def handle_new_hit(forecast, old_hit):

    if not old_hit or not forecast['next_hit']:
        return

    if not find_cell_index_in_history(forecast['hit_history'], old_hit):
        tweet_prediction(forecast['next_hit'])


def schiffts():

    datastorage = DataStorage("schiffts.json")

    # load old data
    old_data = datastorage.load_data()

    current_rain_at_location, forecast, radar_data = get_rain((settings.X_LOCATION, settings.Y_LOCATION),
                                                              old_history=old_data['radar_history'])

    # check if hit was already reported
    # check if old and new rain

    if bool(current_rain_at_location) != bool(old_data['rain_at_position']):
        do_twitter(current_rain_at_location)

    save_data(datastorage, current_rain_at_location, radar_data, forecast['next_hit'])

    save_cells(radar_data[0].cells, False)


if __name__ == '__main__':
    schiffts()
