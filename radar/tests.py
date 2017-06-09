# -*- coding: utf-8 -*-

import unittest
from datetime import datetime, timedelta

from radar.cell import Cell
from radar.forecast import _find_closest_point, _find_closest_cells, _make_cells_history, _make_cell_history


class RadarDataMock(object):
    def __init__(self, cells, timestamp):
        self.cells = cells
        self.timestamp = timestamp


class ForecastTests(unittest.TestCase):

    def test_closest_point(self):
        point = (5, 5)
        closest = (6, 6)
        candidates = [
            (0, 0),
            (3, 6),
            closest,
            (4, 2)
        ]

        closest_point_index, dist = _find_closest_point(point, candidates)
        index = candidates.index(closest)
        self.assertEqual(closest_point_index, index)

    def test_find_closest_cells(self):
        cell1 = Cell(23, 30, 23, (5, 5), [255, 255, 255], "test1", 12344565)
        cell2 = Cell(23, 30, 23, (10, 10), [255, 255, 255], "test2", 12344565)

        old_cell1 = Cell(23, 30, 23, (10, 12), [255, 255, 255], "test3", 12340000)
        old_cell2 = Cell(23, 30, 23, (6, 6), [255, 255, 255], "test4", 12340000)
        old_cell3 = Cell(23, 30, 23, (4, 3), [255, 255, 255], "test5", 12340000)
        old_cell4 = Cell(23, 30, 23, (15, 15), [255, 255, 255], "test6", 12340000)

        cells = [cell1, cell2]
        cells_n_minus_1 = [old_cell1, old_cell2, old_cell3, old_cell4]

        expected_cells = [old_cell2, old_cell1]
        self.assertEqual(expected_cells, _find_closest_cells(cells, cells_n_minus_1))

    def test_filter_closest_cells(self):
        cell1 = Cell(23, 30, 23, (0, 0), [255, 255, 255], "test1", 12344565)

        old_cell1 = Cell(23, 30, 23, (4.1, 4.1), [255, 255, 255], "test2", 12340000)

        cells = [cell1]
        cells_n_minus_1 = [old_cell1]

        expected_cells = [None]
        self.assertEqual(expected_cells, _find_closest_cells(cells, cells_n_minus_1))

    def test_filter_no_old_cells(self):
        cell1 = Cell(23, 30, 23, (0, 0), [255, 255, 255], "test1", 12344565)

        cells = [cell1]
        cells_n_minus_1 = []

        expected_cells = [None]
        self.assertEqual(expected_cells, _find_closest_cells(cells, cells_n_minus_1))

    def test_make_cell_history(self):
        cells_data = [
            ["cell11", "cell21", "cell31"],
            ["cell12", "cell22", "cell32"],
            ["cell13", "cell23", "cell33"],
            ["cell14", "cell24", "cell34"],
        ]

        cells_history = _make_cell_history(cells_data)

        expected_data = [
            ["cell11", "cell12", "cell13", "cell14"],
            ["cell21", "cell22", "cell23", "cell24"],
            ["cell31", "cell32", "cell33", "cell34"]
        ]

        self.assertEqual(cells_history, expected_data)

    def test_make_cell_history_with_missing(self):

        cells_data = [
            ["cell11", "cell21", "cell31"],
            ["cell12", "cell22", None],
            ["cell13", None, "cell33"],
            ["cell14", "cell24", "cell34"],
        ]

        cells_history = _make_cell_history(cells_data)

        expected_data = [
            ["cell11", "cell12", "cell13", "cell14"],
            ["cell21", "cell22"],
            ["cell31"]
        ]

        self.assertEqual(cells_history, expected_data)

    # def test_make_cells_history(self):
    #     # cells at t
    #     t = datetime.now()
    #     cell1 = Cell(23, 30, 23, (5, 5), [255, 255, 255], "test1", t)
    #     cell2 = Cell(23, 30, 23, (10, 10), [255, 255, 255], "test2", t)
    #
    #     current_cells = [cell1, cell2]
    #
    #     radar_data_t = RadarDataMock(current_cells, t)
    #
    #     #cells at t2
    #     t2 = t - timedelta(0, 4 * 60)
    #     cell3 = Cell(23, 30, 23, (12, 12), [255, 255, 255], "test3", t)
    #     cell4 = Cell(23, 30, 23, (4, 4), [255, 255, 255], "test4", t)
    #
    #     radar_data_t2 = RadarDataMock([cell3, cell4], t2)
    #
    #     #cells at t3
    #     t3 = t - timedelta(0, 8 * 60)
    #     cell5 = Cell(23, 30, 23, (-1, 0), [255, 255, 255], "test5", t)
    #     cell6 = Cell(23, 30, 23, (12, 12), [255, 255, 255], "test6", t)
    #
    #     radar_data_t3 = RadarDataMock([cell5, cell6], t3)
    #
    #     radar_history = [radar_data_t, radar_data_t2, radar_data_t3]
    #
    #     cells_history = _make_cells_history(radar_history)
    #
    #     print(cells_history)
    #
    #     self.assertEqual(len(cells_history), len(current_cells))
    #     print(cells_history[0][0])
    #
    #     if cells_history[0][0] == cell1:
    #         cells0 = cells_history[0]
    #         cells1 = cells_history[1]
    #     elif cells_history[0][0] == cell2:
    #         cells0 = cells_history[1]
    #         cells1 = cells_history[0]
    #     else:
    #         self.fail("ForecastTests test_make_cells_history: initial cell does not match ({})".format(cells_history[0][0]))
    #
    #     self.assertEqual(cells0, [cell1, cell4])
    #     self.assertEqual(cells1, [cell2, cell3, cell6])


if __name__ == '__main__':
    unittest.main()
