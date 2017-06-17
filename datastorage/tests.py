# -*- coding: utf-8 -*-

import unittest
from numpy import zeros
from datetime import datetime, timedelta

from radar.radar_data import RadarData
from radar.cell import Cell
from datastorage import DataStorage


class DataStorageTests(unittest.TestCase):

    def test_prepare_data(self):
        timestamp1 = datetime.now()
        timestamp2 = timestamp1 + timedelta(0, 60 * 10)
        timestamp3 = timestamp1 + timedelta(0, 60 * 20)
        timestamp4 = timestamp1 + timedelta(0, 60 * 40)

        cells11 = Cell(23, 30, 23, (5, 5), [255, 255, 255], "cells11", timestamp1)
        cells12 = Cell(23, 30, 23, (10, 10), [255, 255, 255], "cells12", timestamp1)

        cells21 = Cell(23, 30, 23, (10, 12), [255, 255, 255], "cells21", timestamp2)
        cells22 = Cell(23, 30, 23, (6, 6), [255, 255, 255], "cells22", timestamp2)
        cells23 = Cell(23, 30, 23, (4, 3), [255, 255, 255], "cells23", timestamp2)
        cells24 = Cell(23, 30, 23, (15, 15), [255, 255, 255], "cells24", timestamp2)

        cells31 = Cell(23, 30, 23, (10, 12), [255, 255, 255], "cells31", timestamp3)
        cells32 = Cell(23, 30, 23, (6, 6), [255, 255, 255], "cells32", timestamp3)
        cells33 = Cell(23, 30, 23, (4, 3), [255, 255, 255], "cells33", timestamp3)

        next_hit = Cell(23, 30, 23, (4, 3), [255, 255, 255], "next", timestamp4)

        cells1 = [cells11, cells12]
        cells2 = [cells21, cells22, cells23, cells24]
        cells3 = [cells31, cells32, cells33]

        radar_data1 = RadarData(None, timestamp1)
        radar_data1.cells = cells1
        radar_data1.label_image = zeros(shape=(2, 2))

        radar_data2 = RadarData(None, timestamp2)
        radar_data2.cells = cells2
        radar_data2.label_image = zeros(shape=(2, 2))

        radar_data3 = RadarData(None, timestamp3)
        radar_data3.cells = cells3
        radar_data3.label_image = zeros(shape=(2, 2))

        current_rain = {'name': '3mm/h', 'rgb': [0, 50, 255], 'intensity': 1}

        storage = DataStorage("some.json")

        radar_history = [radar_data1, radar_data2, radar_data3]

        data = storage._prepare_data(timestamp1, radar_history, next_hit, current_rain)

        expected_data = {
            'timestamp': timestamp1,
            'radar_history': [radar_data1.to_dict(), radar_data2.to_dict(), radar_data3.to_dict()],
            'next_hit': next_hit.to_dict(),
            'rain_at_position': current_rain
        }

        self.assertEqual(data, expected_data)


class DataStorageTests(unittest.TestCase):

    def test_prepare_data_empty_history(self):
        timestamp1 = datetime.now()
        timestamp2 = timestamp1 + timedelta(0, 60 * 10)

        radar_data1 = RadarData(None, timestamp1)
        radar_data1.cells = []
        radar_data1.label_image = zeros(shape=(2, 2))

        radar_data2 = RadarData(None, timestamp2)
        radar_data2.cells = []
        radar_data2.label_image = zeros(shape=(2, 2))

        next_hit = Cell(23, 30, 23, (4, 3), [255, 255, 255], "next", timestamp2)


        current_rain = {'name': '3mm/h', 'rgb': [0, 50, 255], 'intensity': 1}

        storage = DataStorage("some.json")

        radar_history = [radar_data1, radar_data2]

        data = storage._prepare_data(timestamp1, radar_history, next_hit, current_rain)

        expected_data = {
            'timestamp': timestamp1,
            'radar_history': [radar_data1.to_dict(), radar_data2.to_dict()],
            'next_hit': next_hit.to_dict(),
            'rain_at_position': current_rain
        }

        self.assertEqual(data, expected_data)
