# -*- coding: utf-8 -*-
from radar.radar_data import RadarData
from radar.radar_image import RadarImage
from radar.utils import create_last_radar_timestamp, create_past_timestamps
from radar.forecast import make_forecast

HALF_TEST_FIELD_SIZE = int(104/2)
DATE_FORMAT = "%Y%m%d%H%M00"  # todo: use this one


def get_rain(location):
    timestamp = create_last_radar_timestamp()
    timestamps = [timestamp] + create_past_timestamps(timestamp, 2)

    radar_history = []

    for timestamp in timestamps:
        radar_img = RadarImage((location[0] - HALF_TEST_FIELD_SIZE, location[1] - HALF_TEST_FIELD_SIZE,
                                location[0] + HALF_TEST_FIELD_SIZE, location[1] + HALF_TEST_FIELD_SIZE),
                                timestamp=timestamp)

        radar_data_for_timestamp = RadarData(radar_img, timestamp)
        radar_history.append(radar_data_for_timestamp)

    current_radar_data = radar_history[0]
    current_data_at_position = current_radar_data.rain_at_position(HALF_TEST_FIELD_SIZE, HALF_TEST_FIELD_SIZE)
    forecast = make_forecast(radar_history, location)

    return current_data_at_position, forecast, radar_history
