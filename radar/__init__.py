# -*- coding: utf-8 -*-

from radar.radar_data import RadarData
from radar.radar_image import RadarImage
from radar.utils import create_last_radar_timestamp, create_past_timestamps
from radar.forecast import make_forecast

HALF_TEST_FIELD_SIZE = int(104/2)
DATE_FORMAT = "%Y%m%d%H%M00"  # todo: use this one


def _find_radar_data_in_history_for_timestamp(timestamp, saved_history):
    return next((radar for radar in saved_history if radar.timestamp == timestamp), None)


def _calculate_crop_bounding_coords(location_coords):
    return (location_coords[0] - HALF_TEST_FIELD_SIZE, location_coords[1] - HALF_TEST_FIELD_SIZE,
            location_coords[0] + HALF_TEST_FIELD_SIZE, location_coords[1] + HALF_TEST_FIELD_SIZE)


def _collect_rain_data_for_timestamp(saved_history, timestamp, location_bounding_coords):

    radar_data_for_timestamp = None

    if saved_history:
        radar_data_for_timestamp = _find_radar_data_in_history_for_timestamp(timestamp, saved_history)
    if not radar_data_for_timestamp:
        radar_img = RadarImage(location_bounding_coords, timestamp=timestamp)

        radar_data_for_timestamp = RadarData(radar_img, timestamp)

    return radar_data_for_timestamp


def collect_rain_data(location_coords, saved_history=None):
    timestamp = create_last_radar_timestamp()
    timestamps = [timestamp] + create_past_timestamps(timestamp, 1)
    location_bounding_coords = _calculate_crop_bounding_coords(location_coords)

    radar_history = []

    for timestamp in timestamps:
        radar_data_for_timestamp = _collect_rain_data_for_timestamp(saved_history, timestamp, location_bounding_coords)
        radar_history.append(radar_data_for_timestamp)

    current_radar_data = radar_history[0]
    current_data_at_position = current_radar_data.rain_at_position(HALF_TEST_FIELD_SIZE, HALF_TEST_FIELD_SIZE)
    forecast = make_forecast(radar_history, (HALF_TEST_FIELD_SIZE, HALF_TEST_FIELD_SIZE))

    return current_data_at_position, forecast, radar_history
