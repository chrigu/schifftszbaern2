# # -*- coding: utf-8 -*-
import os
import unittest
import settings
from radar import HALF_TEST_FIELD_SIZE, RadarData, make_forecast

from radar import create_last_radar_timestamp, create_past_timestamps, RadarImage


class ImageTests(unittest.TestCase):

    def get_rain(self, images):
        timestamp = create_last_radar_timestamp()
        timestamps = [timestamp] + create_past_timestamps(timestamp, len(images)-1)

        location = (settings.X_LOCATION, settings.Y_LOCATION)

        radar_history = []

        for index, timestamp in enumerate(timestamps):

            url = 'file:{}/test_images/{}'.format(os.path.dirname(os.path.realpath(__file__)), images[index])
            radar_img = RadarImage((location[0] - HALF_TEST_FIELD_SIZE, location[1] - HALF_TEST_FIELD_SIZE,
                                    location[0] + HALF_TEST_FIELD_SIZE, location[1] + HALF_TEST_FIELD_SIZE),
                                    timestamp=timestamp, url=url)

            radar_data_for_timestamp = RadarData(radar_img, timestamp)
            radar_history.append(radar_data_for_timestamp)

        current_radar_data = radar_history[0]
        current_data_at_position = current_radar_data.rain_at_position(HALF_TEST_FIELD_SIZE, HALF_TEST_FIELD_SIZE)
        forecast = make_forecast(radar_history, (HALF_TEST_FIELD_SIZE, HALF_TEST_FIELD_SIZE))

        return current_data_at_position, forecast, radar_history

    def test_image(self):
        self.get_rain(['1.png', '0.png'])
