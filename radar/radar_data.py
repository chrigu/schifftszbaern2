# -*- coding: utf-8 -*-
import settings
from datetime import datetime

from numpy import array as np_array
from scipy import ndimage
# import matplotlib.pyplot as plt
import numpy as np
from numpy import linalg

from radar.utils import DATE_FORMAT
from radar.cell import Cell

#todo move to const


RAIN_INTENSITIES = [{'name': '1mm/h', 'rgb': [0, 150, 255], 'intensity': 0},
                    {'name': '3mm/h', 'rgb': [0, 50, 255], 'intensity': 1},
                    {'name': '10mm/h', 'rgb': [0, 0, 200], 'intensity': 2},
                    {'name': '30mm/h', 'rgb': [0, 0, 125], 'intensity': 3},
                    {'name': '100mm/h', 'rgb': [255, 255, 0], 'intensity': 4},
                    {'name': '>100mm/h', 'rgb': [255, 0, 0], 'intensity': 5},
                    {'name': 'flakes', 'rgb': [200, 255, 255], 'intensity': 10},
                    {'name': 'snow weak', 'rgb': [150, 255, 255], 'intensity': 11},
                    {'name': 'snow moderate', 'rgb': [100, 255, 255], 'intensity': 12},
                    {'name': 'snow strong', 'rgb': [25, 255, 255], 'intensity': 13},
                    {'name': 'snow heavy', 'rgb': [0, 255, 255], 'intensity': 14},
                    {'name': 'snow very heavy', 'rgb': [0, 200, 255], 'intensity': 15},
                    {'name': 'blank', 'rgb': [9, 46, 69], 'intensity': -1}]


class RadarData(object):
    """
    Contains rain information for the whole area for a given time

    PNG info:

    1px = approx. 850m

    *******

    radar values:

    < 1mm/h   0/150/255
    < 3mm/h   0/50/255
    < 10mm/h  0/0/200
    < 30mm/h  0/0/125
    < 100mm/h 255/255/0
    > 100mm/h 255/0/0

    Flocken 199/254/254
    schwach 150/255/255
    mässig 100/255/255
    stark 25/255/255
    sehr stark 0/255/255
    extrem 0/200/255


    """
    def __init__(self, radar_image, timestamp):

        self.radar_image = radar_image
        self.timestamp = timestamp

        if self.radar_image:
            image_data = self._make_raster(radar_image.image_data)
            self.cells, self.label_image = self._analyze(image_data)

    def __str__(self):
        return self.timestamp

    # def __unicode__(self):
    #     return u"%s" % self.timestamp
    #
    def to_dict(self):

        dict_cells = []

        for cell in self.cells:
            dict_cells.append(cell.to_dict())

        label_image = self.label_image

        if not isinstance(label_image, list):
            label_image = self.label_image.tolist()

        return_dict = {
            'cells': dict_cells,
            'label_image': label_image,
            'timestamp': datetime.strftime(self.timestamp, DATE_FORMAT)
        }

        return return_dict

    @staticmethod
    def from_dict(data_dict):

        radar_data = RadarData(None, datetime.strptime(data_dict['timestamp'], DATE_FORMAT))

        cells = []

        for cell_dict in data_dict['cells']:
            if bool(cell_dict):
                cell = Cell.from_dict(cell_dict)
                cells.append(cell)

        radar_data.cells = cells
        radar_data.label_image = data_dict['label_image']

        return radar_data

    #
    # def to_json(self):
    #     return json.dumps(self.to_dict())

    def rain_at_position(self, x, y):
        """
        Get rain intensity for position at x, y
        """

        if not self.radar_image:
            return None

        pixels = []

        rgb_values = [0, 0, 0]
        for y_pos in range(y - 1, y + 2):
            for x_pos in range(x - 1, x + 2):

                pixel = self.radar_image.get_rgb_for_position((x, y))
                pixels.append(pixel)

                for i in range(0, 3):
                    rgb_values[i] += pixel[i]

        max_value = max(pixels, key=tuple)
        return self._get_intensity(max_value) or None

    def _get_intensity(self, rgb_vector):
        """
        Finds the closest matching intensity for a given color
        """
        # rgb_vector needs to have some minimal length
        if linalg.norm(rgb_vector, ord=1) < 50:
            return None

        # calculate the distance to all intensities & find the minimal distance
        distances = list(map(
            lambda value: linalg.norm(rgb_vector - np_array((value['rgb'][0], value['rgb'][1], value['rgb'][2]))),
            RAIN_INTENSITIES))
        min_distance = min(distances)

        # just check that the distance is reasonable
        if int(min_distance) < 200:
            intensity = RAIN_INTENSITIES[distances.index(min(distances))]
            # check if blank image was shown:
            if intensity['intensity'] != -1:
                return intensity
        else:
            return None

    def _get_color_values(self, pixel_x, pixel_y):
        """
        Returns r,g,b for a given pixel. Omits alpha data.
        """
        print(self.radar_image.get_rgb_for_position((0, 0)))
        if self.radar_image._has_alpha:
            factor = 4
        else:
            factor = 3
        if not self.radar_image._has_alpha or (self.radar_image._image_data[pixel_y][pixel_x * factor + 3] > 0):
            return [self.radar_image._image_data[pixel_y][pixel_x * factor],
                    self.radar_image._image_data[pixel_y][pixel_x * factor + 1],
                    self.radar_image._image_data[pixel_y][pixel_x * factor + 2]]
        else:
            return [0, 0, 0]

    def get_data_for_label(self, label):
        for data in self.cells:
            if data['label'] == label:
                return data
        return None

    def _make_raster(self, pixel_array):
        """
        Downsamples the image (pixel_array) so that it is =
         test_field_width/self.raster_width * test_field_width/self.raster_width in size.
        """
        #todo: do better

        image_array = []

        for row in pixel_array:
            new_row = []
            for pixel in row:
                new_pixel = self._get_non_alpha(pixel)
                new_row.append(new_pixel)
            image_array.append(new_row)

        return image_array

    def _get_non_alpha(self, pixel):
        """
        Removes alpha from pixel
        :param pixel: 
        :return: new pixel without Alpha Channel
        """
        if len(pixel) == 4 and pixel[3] > 127:
            new_pixel = [pixel[0], pixel[1], pixel[2]]
        else:
            new_pixel = [0, 0, 0]

        return new_pixel

    def _make_mask(self, data):
        # create array that only indicates regions (ie raincells), so that for a given x and y 1 = rain and 0 = no rain
        out = []

        for row in data:
            a = []
            for pixel in row:
                if pixel.any():
                    a.append(1)
                else:
                    a.append(0)

            out.append(a)

        return np.array(out)

    def _get_raincell_data(self, regions_data):
        # calculate position & size of the raincells (raincells are simplified (circular shape))
        mask = regions_data
        label_image, nb_labels = ndimage.label(regions_data)
        # self.img_data = np.array(test)
        sizes = ndimage.sum(regions_data, label_image, index=range(0, nb_labels+1))
        mean_values = ndimage.sum(regions_data, label_image, index=range(0, nb_labels+1))
        masses = ndimage.center_of_mass(mask, labels=label_image, index=range(0, nb_labels+1))

        cell_data = []

        for i in range(0, len(sizes)):
            cell = {
                'size': sizes[i],
                'mean': mean_values[i],
                'mass': masses[i]
            }
            cell_data.append(cell)

        return cell_data, nb_labels, label_image

    def _color_for_cell(self, labels, label_image, image):
        """
        group pixels that belong to labels (cell)
        """

        cell_rgb = []
        for n in range(0, labels+1):
            cell_rgb.append([0, 0, 0])

        # calcualte color value for regions
        y = 0
        for line in label_image:
            x = 0
            for label in line:
                if label != 0:
                    for color in range(0, 3):
                        cell_rgb[label.astype(int)][color] += image[y][x][color]
                x += 1
            y += 1

        return cell_rgb


    def _analyze(self, data):
        """
        Finds raincells and calculates center of mass & size for each cell.
        Returns an array with the raincells.
        """
        image = np.array(data)
        regions_data = self._make_mask(image)
        cell_data, labels, label_image = self._get_raincell_data(regions_data)

        cells_rgb = self._color_for_cell(labels, label_image, image)
        result = []

        # calculate average color value for regions and map it to the raincell
        # construct array with all data
        for n in range(0, labels+1):

            if cell_data[n]['size'] == 0:
                continue

            cell_rgb = []
            for m in range(0, 3):
                cell_rgb.append(cells_rgb[n][m]/cell_data[n]['mean'])

            # TODO: fix intensity!
            intensity = self._get_intensity(np_array([round(cell_rgb[0]), round(cell_rgb[1]),
                                                    round(cell_rgb[2])]))

            cell = Cell(intensity, cell_data[n]['size'], cell_data[n]['mean'],
                        [cell_data[n]['mass'][0], cell_data[n]['mass'][1]], cell_rgb, n,
                        self.timestamp)

            result.append(cell)

        return result, label_image

