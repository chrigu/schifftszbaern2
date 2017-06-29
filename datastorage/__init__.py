# -*- coding: utf-8 -*-
import json

from radar.radar_data import RadarData
from radar.cell import Cell

class DataStorage(object):

    def __init__(self, filename):
        self.filename = filename

    def _prepare_data(self, timestamp, radar_history, next_hit, rain_at_pos):

        radar_history_dicts = list(map(lambda radar_data: radar_data.to_dict(), radar_history))

        next_hit_dict = {}

        if next_hit:
            next_hit_dict = next_hit.to_dict()

        data = {
            'timestamp': timestamp,
            'radar_history': radar_history_dicts,
            'next_hit': next_hit_dict,
            'rain_at_position': rain_at_pos
        }
        return data

    def _read_data(self):

        loaded_data = None

        try:
            f = open(self.filename, 'r')
            loaded_data = json.loads(f.read())

        except Exception as e:
            print(e)

        finally:
            try:
                f.close()
            except:
                pass

        return loaded_data

    def load_data(self):
        # try to open the file with the old data

        data = {
            'timestamp': None,
            'radar_history': [],
            'next_hit': None,
            'rain_at_position': None
        }

        old_data = self._read_data()
        if not old_data:
            return data

        if 'timestamp' in old_data:
            data['timestamp'] = old_data['timestamp']

        if 'radar_history' in old_data:

            radar_history = []

            for radar_data in old_data['radar_history']:
                radar_history.append((RadarData.from_dict(radar_data)))

            data['radar_history'] = radar_history

        if 'rain_at_position' in old_data:
            data['rain_at_position'] = old_data['rain_at_position']

        if 'next_hit' in old_data and bool(old_data['next_hit']):
            data['next_hit'] = Cell.from_dict(old_data['next_hit'])

        return data

    def save_data(self, timestamp, radar_history, next_hit, rain_at_pos):
        rain_data = self._prepare_data(timestamp, radar_history, next_hit, rain_at_pos)

        try:
            with open(self.filename, 'w') as outfile:
                json.dump(rain_data, outfile)

            return True

        except Exception:
            print("Could not write json")
            return False
