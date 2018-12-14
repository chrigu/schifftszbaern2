# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta

from radar import RadarData, _find_radar_data_in_history_for_timestamp


class RadarTests(unittest.TestCase):

    def test_get_saved_radar_data(self):

        timestamps = [datetime.now() + timedelta(0, x * -10 * 60) for x in range(3)]
        radar_history = [RadarData(None, timestamp) for timestamp in timestamps]

        radar_data = _find_radar_data_in_history_for_timestamp(timestamps[1], radar_history)

        self.assertEqual(radar_data, radar_history[1])

    def test_get_saved_radar_data_without_result(self):

        timestamps = [datetime.now() + timedelta(0, x * -10 * 60) for x in range(3)]
        radar_history = [RadarData(None, timestamp) for timestamp in timestamps]

        radar_data = _find_radar_data_in_history_for_timestamp(datetime.now() + timedelta(0, 5 * -10 * 60), radar_history)

        self.assertEqual(radar_data, None)
