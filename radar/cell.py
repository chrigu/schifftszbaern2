# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from radar.utils import DATE_FORMAT


class Cell(object):

    def __init__(self, intensity, size, mean, center_of_mass, rgb, label, timestamp, cell_id=None):
        self.intensity = intensity
        self.size = size
        self.mean = mean
        self.center_of_mass = center_of_mass
        self.rgb = rgb
        self.label = label
        if cell_id:
            self.id = cell_id
        else:
            self.id = uuid.uuid4().hex
        self.timestamp = timestamp  # todo: needed?

    def __str__(self):
        return self.label

    def __repr__(self):
        return self.label

    def to_dict(self):
        return {
            'intensity': self.intensity,
            'size': self.size,
            'mean': self.mean,
            'center_of_mass': {
                'x': self.center_of_mass[0],
                'y': self.center_of_mass[1]
            },
            'rgb': self.rgb,
            'label': self.label,
            'id': self.id,
            'timestamp': datetime.strftime(self.timestamp, DATE_FORMAT)
        }

    @staticmethod
    def from_dict(cell_dict):
        return Cell(cell_dict['intensity'], cell_dict['size'], cell_dict['mean'],
                    (cell_dict['center_of_mass'][0], cell_dict['center_of_mass'][1], cell_dict['rgb']),
                    cell_dict['label'], datetime.strptime(str(cell_dict['timsestamp']), DATE_FORMAT), cell_dict['id'])
