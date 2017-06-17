# -*- coding: utf-8 -*-

import unittest
import math
from datetime import datetime, timedelta

from radar.cell import Cell
from radar.forecast import _find_closest_point, _find_closest_cells, _make_cells_history, _make_cell_history, \
    _get_delta_for_cell_history, _extrapolate_cells, _calc_next_positions, _find_next_hit, _find_cell_hits, \
    _find_forecasts_index_for_next_hit


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
        cell1 = Cell(23, 30, 23, (5, 5), [255, 255, 255], "cell1", 12344565)
        cell2 = Cell(23, 30, 23, (10, 10), [255, 255, 255], "cell2", 12344565)

        old_cell1 = Cell(23, 30, 23, (10, 12), [255, 255, 255], "old_cell1", 12340000)
        old_cell2 = Cell(23, 30, 23, (6, 6), [255, 255, 255], "old_cell2", 12340000)
        old_cell3 = Cell(23, 30, 23, (4, 3), [255, 255, 255], "old_cell3", 12340000)
        old_cell4 = Cell(23, 30, 23, (15, 15), [255, 255, 255], "old_cell4", 12340000)

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

    def test_make_cells_history(self):
        # cells at t
        t = datetime.now()
        cell1 = Cell(23, 30, 23, (5, 5), [255, 255, 255], "test1", t)
        cell2 = Cell(23, 30, 23, (10, 10), [255, 255, 255], "test2", t)

        current_cells = [cell1, cell2]

        radar_data_t = RadarDataMock(current_cells, t)

        #cells at t2
        t2 = t - timedelta(0, 4 * 60)
        cell3 = Cell(23, 30, 23, (12, 12), [255, 255, 255], "test3", t)
        cell4 = Cell(23, 30, 23, (4, 4), [255, 255, 255], "test4", t)

        radar_data_t2 = RadarDataMock([cell3, cell4], t2)

        #cells at t3
        t3 = t - timedelta(0, 8 * 60)
        cell5 = Cell(23, 30, 23, (-1, 0), [255, 255, 255], "test5", t)
        cell6 = Cell(23, 30, 23, (12, 14), [255, 255, 255], "test6", t)

        radar_data_t3 = RadarDataMock([cell5, cell6], t3)

        radar_history = [radar_data_t, radar_data_t2, radar_data_t3]

        cells_history = _make_cells_history(radar_history)

        self.assertEqual(len(cells_history), len(current_cells))

        if cells_history[0][0] == cell1:
            cells0 = cells_history[0]
            cells1 = cells_history[1]
        elif cells_history[0][0] == cell2:
            cells0 = cells_history[1]
            cells1 = cells_history[0]
        else:
            self.fail("ForecastTests test_make_cells_history: initial cell does not match ({})".format(cells_history[0][0]))

        self.assertEqual(cells0, [cell1, cell4])
        self.assertEqual(cells1, [cell2, cell3, cell6])

    def test_get_delta_for_cell_history(self):

        first_x, first_y, last_x, last_y = 0, 0, 10, 10

        t = datetime.now()
        cell1 = Cell(23, 30, 23, (first_x, first_y), [255, 255, 255], "test1", t)
        cell2 = Cell(23, 30, 23, (5, 10), [255, 255, 255], "test2", t)
        cell3 = Cell(23, 30, 23, (last_x, last_y), [255, 255, 255], "test3", t)

        cell_history = [cell1, cell2, cell3]

        expected_delta_x = (last_x - first_x) / len(cell_history)
        expected_delta_y = (last_y - first_y) / len(cell_history)

        delta_x, delta_y = _get_delta_for_cell_history(cell_history)

        self.assertEqual(delta_x, expected_delta_x)
        self.assertEqual(delta_y, expected_delta_y)

    def test_calc_next_positions(self):

        x, y = 0, 10
        delta_x = 2
        delta_y = 5
        n = 3

        t = datetime.now()
        cell1 = Cell(23, 30, 23, (x, y), [255, 255, 255], "test1", t)

        forecast = _calc_next_positions(cell1, delta_x, delta_y, n)

        self.assertEqual(len(forecast), n)

        index = 1

        for future_cell in forecast:
            self.assertEqual(future_cell.center_of_mass, (x + delta_x * index, y + delta_y * index))
            index += 1

    def test_find_next_hit(self):

        cell1 = Cell(23, 30, 23, (5, 10), [255, 255, 255], "test1", 1000)
        cell2 = Cell(23, 30, 23, (5, 10), [255, 255, 255], "test2", 100)
        cell3 = Cell(23, 30, 23, (5, 10), [255, 255, 255], "test3", 10000)

        closest_hit = _find_next_hit([cell1, cell2, cell3])

        self.assertEqual(cell2, closest_hit)

    def test_find_next_hit_no_hit(self):

        closest_hit = _find_next_hit([])

        self.assertEqual(None, closest_hit)

    def test_cell_hits(self):

        location = (10, 10)

        r1 = math.pi * 1
        r2 = math.pi * 2 ** 2
        r3 = r2

        hit1 = Cell(23, r2, 23, (10, 8.1), [255, 255, 255], "hit1", 30000)
        hit2 = Cell(23, r3, 23, (8.1, 10), [255, 255, 255], "hit2", 30000)

        cells1 = [
            Cell(23, r1, 23, (2, 2), [255, 255, 255], "test1", 10000),
            Cell(23, r1, 23, (4, 4), [255, 255, 255], "test2", 20000),
            Cell(23, r1, 23, (6, 6), [255, 255, 255], "test3", 30000),
        ]

        cells2 = [
            Cell(23, r2, 23, (10, 4), [255, 255, 255], "test4", 10000),
            Cell(23, r2, 23, (10, 6), [255, 255, 255], "test5", 20000),
            hit1,
        ]

        cells3 = [
            Cell(23, r3, 23, (4, 10), [255, 255, 255], "test6", 10000),
            Cell(23, r3, 23, (6, 10), [255, 255, 255], "test7", 20000),
            hit2,
        ]

        forecasted_cells = [cells1, cells2, cells3]

        hits = _find_cell_hits(forecasted_cells, location)

        expected_hits = [hit1, hit2]

        self.assertEqual(hits, expected_hits)

    def test_find_forecasts_index_for_next_hit(self):

        hit1 = Cell(23, 12, 23, (10, 8.1), [255, 255, 255], "hit1", 30000)

        cells1 = [
            Cell(23, 12, 23, (2, 2), [255, 255, 255], "test1", 10000),
            Cell(23, 12, 23, (4, 4), [255, 255, 255], "test2", 20000),
            Cell(23, 12, 23, (6, 6), [255, 255, 255], "test3", 30000),
        ]

        cells2 = [
            Cell(23, 12, 23, (10, 4), [255, 255, 255], "test4", 10000),
            Cell(23, 12, 23, (10, 6), [255, 255, 255], "test5", 20000),
            hit1,
        ]

        cells3 = [
            Cell(23, 12, 23, (4, 10), [255, 255, 255], "test6", 10000),
            Cell(23, 12, 23, (6, 10), [255, 255, 255], "test7", 20000),
            Cell(23, 12, 23, (8.1, 10), [255, 255, 255], "hit2", 30000),
        ]

        forecasted_cells = [cells1, cells2, cells3]

        index = _find_forecasts_index_for_next_hit(forecasted_cells, hit1)

        self.assertEqual(index, 1)

    # def test_extrapolate_cell(self):
    #     first_x, first_y, last_x, last_y = 0, 0, 10, 10
    #
    #     t = datetime.now()
    #     cell1 = Cell(23, 30, 23, (first_x, first_y), [255, 255, 255], "test1", t)
    #     cell2 = Cell(23, 30, 23, (5, 10), [255, 255, 255], "test2", t)
    #     cell3 = Cell(23, 30, 23, (last_x, last_y), [255, 255, 255], "test3", t)
    #
    #     cell4 = Cell(23, 30, 23, (20, 0), [255, 255, 255], "test4", t)
    #     cell5 = Cell(23, 30, 23, (21, 30), [255, 255, 255], "test5", t)
    #     cell6 = Cell(23, 30, 23, (30, 40), [255, 255, 255], "test6", t)
    #
    #     cell_history1 = [cell1, cell2, cell3]
    #     cell_history2 = [cell4, cell5, cell6]
    #
    #     _extrapolate_cells([cell_history1, cell_history2])


if __name__ == '__main__':
    unittest.main()
