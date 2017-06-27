import settings
from datetime import datetime
from radar import get_rain
from radar.utils import DATE_FORMAT
from datastorage import DataStorage


def save_data(datastorage, rain_at_location, radar_data, next_hit):
    current_timestamp = datetime.strftime(radar_data[0].timestamp, DATE_FORMAT)
    datastorage.save_data(current_timestamp, radar_data, next_hit, rain_at_location)


def schiffts():

    datastorage = DataStorage("schiffts.json")

    # load old data
    old_data = datastorage.load_data()

    current_rain_at_location, forecast, radar_data = get_rain((settings.X_LOCATION, settings.Y_LOCATION))

    # save old data to file

    if current_rain_at_location:
        pass
        # tweet or not
        # save
        #

    if forecast['next_hit']:
        pass
        # check in old
        # tweet if new

    save_data(datastorage, current_rain_at_location, radar_data, forecast['next_hit'])


if __name__ == '__main__':
    schiffts()
