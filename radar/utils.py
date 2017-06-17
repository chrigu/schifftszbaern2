from datetime import datetime, timedelta

import settings

DATE_FORMAT = "%Y%m%d%H%M00"


def round_timestamp(time):
    """
    Rounds a given time to the next lower 5minute step.
    """

    # update rate is 5min, so round to the last 5minute step
    off_minutes = time.minute % 5
    rounded_delta = timedelta(0, off_minutes * 60)

    rounded_time = (time - rounded_delta).replace(second=0, microsecond=0)

    return rounded_time


def create_last_radar_timestamp():
    """
    Radar has about a 8 minutes-ish delay. 
    :return: 
    """
    now = datetime.now()
    latest_radar = now - timedelta(0, 10 * 60)  # radar has a 8minute-ish delay, so go 10minutes back in time
    return round_timestamp(latest_radar)


def create_past_timestamps(start_time, num_of_timestamps):
    steps = range(1, num_of_timestamps + 1)
    return list(map(lambda x: (start_time - timedelta(0, 60*5*x)), steps))


def convert_to_timestring(timestamp):
    return datetime.strftime(timestamp, settings.DATE_FORMAT)