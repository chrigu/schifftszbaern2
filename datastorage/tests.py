# -*- coding: utf-8 -*-

import unittest
from mock import patch
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

    # todo: use factory
    @patch.object(DataStorage, '_read_data', return_value={
        'timestamp': "1497949200000",
        'radar_history': [
            {
                'label_image': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                'cells': [
                    {
                        'intensity': 1,
                        'size': 2,
                        'mean': 3,
                        'center_of_mass': (4, 5),
                        'rgb': (6, 7, 8),
                        'label': "test10",
                        'id': 'test_10',
                        'timestamp': "14979492000"
                    },
                    {
                        'intensity': 10,
                        'size': 11,
                        'mean': 12,
                        'center_of_mass': (14, 15),
                        'rgb': (15, 16, 17),
                        'label': "test11",
                        'id': 'test_11',
                        'timestamp': "14979492000"
                    }
                ],
                'timestamp': "14979492000"
            },
            {
                'label_image': [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
                'cells': [
                    {
                        'intensity': 20,
                        'size': 21,
                        'mean': 22,
                        'center_of_mass': (23, 24),
                        'rgb': (25, 26, 27),
                        'label': "test20",
                        'id': 'test_20',
                        'timestamp': "14979491000"
                    },
                    {
                        'intensity': 30,
                        'size': 31,
                        'mean': 32,
                        'center_of_mass': (33, 34),
                        'rgb': (35, 36, 37),
                        'label': "test21",
                        'id': 'test_21',
                        'timestamp': "14979491000"
                    }
                ],
                'timestamp': "14979491000"
            }
        ]
    })
    def test_load_data(self, read_data):
        storage = DataStorage("some.json")
        data = storage.load_data()
        print(data)

        expected_rain = None
        expected_hit = None
        expected_timestamp = '1497949200000'

        radar1 = data['radar_history'][0]
        radar2 = data['radar_history'][1]

        self.assertEqual(data['rain_at_position'], expected_rain)
        self.assertEqual(data['next_hit'], expected_hit)
        self.assertEqual(data['timestamp'], expected_timestamp)

        self.assertEqual(radar1.cells[0].label, "test10")
