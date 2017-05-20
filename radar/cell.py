# -*- coding: utf-8 -*-
import uuid


class Cell(object):

    def __init__(self, intensity, size, mean, center_of_mass, rgb, label):
        self.intensity = intensity
        self.size = size
        self.mean = mean
        self.center_of_mass = center_of_mass
        self.rgb = rgb
        self.label = label
        self.id = uuid.uuid4().hex