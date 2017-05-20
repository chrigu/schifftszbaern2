# -*- coding: utf-8 -*-
from radar.radar_data import RadarData
from radar.radar_image import RadarImage
from radar.utils import create_last_radar_timestamp, create_past_timestamps

HALF_TEST_FIELD_SIZE = int(104/2)

def get_rain(x_location, y_location):
    timestamp = create_last_radar_timestamp()
    timestamps = [timestamp] + create_past_timestamps(timestamp, 2)

    radar_history = []

    for timestamp in timestamps:
        radar_img = RadarImage((x_location - HALF_TEST_FIELD_SIZE, y_location - HALF_TEST_FIELD_SIZE,
                                x_location + HALF_TEST_FIELD_SIZE, y_location + HALF_TEST_FIELD_SIZE),
                                timestamp=timestamp)
        print(radar_img)
        radar_data_for_timestamp = RadarData(radar_img, timestamp)
        radar_history.append(radar_data_for_timestamp)

    current_radar_data = radar_history[0]
    current_data_at_position = current_radar_data.rain_at_position(HALF_TEST_FIELD_SIZE, HALF_TEST_FIELD_SIZE)
    print(current_data_at_position)
