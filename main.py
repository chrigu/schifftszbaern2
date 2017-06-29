import settings
from datetime import datetime
from radar import get_rain
from radar.utils import DATE_FORMAT
from datastorage import DataStorage
from schiffts_twitter.schiffts_twitter import do_twitter


def save_data(datastorage, rain_at_location, radar_data, next_hit):
    current_timestamp = datetime.strftime(radar_data[0].timestamp, DATE_FORMAT)
    datastorage.save_data(current_timestamp, radar_data, next_hit, rain_at_location)


def schiffts():

    datastorage = DataStorage("schiffts.json")

    # load old data
    old_data = datastorage.load_data()

    current_rain_at_location, forecast, radar_data = get_rain((settings.X_LOCATION, settings.Y_LOCATION),
                                                              old_history=old_data['radar_history'])

    # check if hit was already reported
    # check if old and new rain
    # todo: check if timedelta is ok-ish
    # last_update_rain = bool(old_data['rain_at_position'])

    if bool(current_rain_at_location) != bool(old_data['rain_at_position']):
        do_twitter(current_rain_at_location)

    if forecast['next_hit']:
        pass
        # check in old
        # tweet if new

    save_data(datastorage, current_rain_at_location, radar_data, forecast['next_hit'])


if __name__ == '__main__':
    schiffts()
