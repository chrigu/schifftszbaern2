# -*- coding: utf-8 -*-
from datetime import timedelta
from functools import partial


# def _latest_c(reverse_radar_data):
#     oldest_cells = []
#     n_1_values = []
#
#     # add all cells from the oldest radar data object to an array
#     for cell in reverse_radar_data[0].cells:
#         oldest_cells.append([cell])
#         n_1_values.append(cell)
#
#     return oldest_cells, n_1_values
from radar.cell import Cell


def _delta_time_in_tolerance(newer_timestamp, older_timestamp):
    # check if the samples have max. a 10min difference between them.
    dt = newer_timestamp - older_timestamp
    return dt.seconds <= 10 * 60


def _find_closest_point(point, candidates):

    if len(candidates) == 0:
        return -1, -1

    # https://stackoverflow.com/questions/5981502/select-the-closest-pair-from-a-list
    dist = lambda s, d: (s[0] - d[0]) ** 2 + (s[1] - d[1]) ** 2
    min_point = min(candidates, key=partial(dist, point))
    closest_index = candidates.index(min_point)
    return closest_index, dist(point, min_point)


def _find_closest_point_and_filter_by_distance(point, candidates, max_distance):

    if len(candidates) == 0:
        return -1

    closest_index, dist = _find_closest_point(point, candidates)

    if dist <= max_distance ** 2:
        return closest_index
    else:
        return -1


def _find_closest_cells(cells_at_n, cells_at_n_minus_1):

    closest_cells = []
    positions_n_minus_1 = list(map(lambda old_cell: old_cell.center_of_mass, cells_at_n_minus_1))
    for cell in cells_at_n:
        # just some treshold (about 9.6km (if delta is 5 minutes this is about 115km/h))
        closest_index = _find_closest_point_and_filter_by_distance(cell.center_of_mass, positions_n_minus_1, 4)
        if closest_index > -1:
            closest_cells.append(cells_at_n_minus_1[closest_index])
        else:
            closest_cells.append(None)

    return closest_cells


def _make_cell_history(cells_data):
    # creates a history for each rain cell

    if len(cells_data) == 0:
        return []

    histories = []
    number_cells = len(cells_data[0])

    # todo: generator time?
    for cell_index in range(0, number_cells):
        for point_in_time_index in range(0, len(cells_data)):
            if point_in_time_index == 0:
                histories.append([cells_data[0][cell_index]])
            elif cells_data[point_in_time_index][cell_index]:
                histories[cell_index].append(cells_data[point_in_time_index][cell_index])
            else:
                break

    return histories


def _make_cells_history(radar_data):
    if len(radar_data) < 2:
        return

    # init closest cells with latest cells from radar
    closest_cells = radar_data[0].cells

    cells_history = [closest_cells]

    for index in range(1, len(radar_data)):
        older_cells = radar_data[index].cells
        if _delta_time_in_tolerance(radar_data[index - 1].timestamp, radar_data[index].timestamp):
            closest_cells = _find_closest_cells(closest_cells, older_cells)
            cells_history.append(closest_cells)

    return _make_cell_history(cells_history)


def _get_delta_for_cell_history(cell_history):
    number_items = len(cell_history)
    delta_x = (cell_history[-1].center_of_mass[0] - cell_history[0].center_of_mass[0]) / number_items
    delta_y = (cell_history[-1].center_of_mass[1] - cell_history[0].center_of_mass[1]) / number_items

    return delta_x, delta_y


def _calc_next_positions(cell, delta_x, delta_y, steps):

    forecasts = []

    for index in range(1, steps + 1):

        delta_t = 10 * 60 * index # assume it's always a 10min step (for starters)
        future_position = (cell.center_of_mass[0] + delta_x * index, cell.center_of_mass[1] + delta_y * index)
        forecast_cell = Cell(cell.intensity, cell.size, cell.mean, future_position, cell.rgb,
                             'forecast_{}'.format(cell.label), cell.timestamp + timedelta(0, delta_t))

        forecasts.append(forecast_cell)
        # print(forecast_cell.center_of_mass)

    return forecasts


def _extrapolate_cells(cells_history):
    # calc 5 next points
    for cell_history in cells_history:
        delta_x, delta_y = _get_delta_for_cell_history(cell_history)
        forecasted_cells = _calc_next_positions(cell_history[-1], delta_x, delta_y, 5)
        print(forecasted_cells)
    pass

def make_forecast(radar_data):

    cells_history = _make_cells_history(radar_data)
    # extra polate points
    # check if hit near point & which hit // closest hit



    # loop through radar data
    # find closest cells array in array


    # # oldest sample first in array
    # reverse_radar_data = sorted(radar_data, key=lambda x: x.timestamp, reverse=True)
    # history = None
    #
    # new_data, n_1_values = _init_samples(reverse_radar_data)
    #
    # # go through the rest of the data (time descending)
    # for index in range(1, len(reverse_radar_data)):
    #     # check if the samples have max. a 10min difference between them.
    #     try:
    #         dt = reverse_radar_data[index - 1].timestamp - reverse_radar_data[index].timestamp
    #
    #         if dt.seconds > 10 * 60:
    #             break
    #
    #     except Exception as e:
    #         print("error: {}".format(e))
    #         continue
    #
    #     close_points = _find_closest_old_cells(data[index], n_1_values)
    #     history = _add_to_closest_match_to_history(data[index], n_1_values, close_points, new_data)
    #
    #     n_1_values = data[index].data
    #
    # # todo: fix parameters
    # return _caclulate_vector(new_data), history # history and new_data is kind of the same o_O