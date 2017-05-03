# -*- coding: utf-8 -*-

import scipy.misc
import gdal
import math
import numpy

from skimage.color import rgb2gray


class TifHandler(object):

    def __init__(self, tif_path):
        self._dataset = gdal.Open(tif_path)
        self._gt = self._dataset.GetGeoTransform()
        self._im = rgb2gray(scipy.misc.imread(tif_path))
        self._world_size = None

    @property
    def world_size(self):
        if not self._world_size:
            point_1 = numpy.array(self.image_coordinate(0, 0))
            point_2 = numpy.array(self.image_coordinate(180, 90))
            self._world_size = tuple((abs(point_2) + abs(point_1)) * 2)
        return self._world_size

    def image_coordinate(self, longtitude, latitude):
        gt = self._gt
        image_x = float((longtitude * gt[4] - latitude * gt[1] - gt[0] * gt[4] + gt[1] * gt[3]) /
                        (gt[2] * gt[4] - gt[1] * gt[5]))
        image_y = float((longtitude * gt[5] - latitude * gt[2] - gt[0] * gt[5] + gt[2] * gt[3]) /
                        (gt[1] * gt[5] - gt[2] * gt[4]))
        image_x = int(image_x+0.5)
        image_y = int(image_y+0.5)
        return image_x, image_y

    def geo_coordinate(self, image_x, image_y):
        geo_x = self._gt[0] + image_x * self._gt[1] + image_y * self._gt[2]
        geo_y = self._gt[3] + image_x * self._gt[4] + image_y * self._gt[5]
        return geo_x, geo_y

    def get_brightness(self, longtitude, latitude, size):
        r, max_light = 6371, 1.0
        im_x, im_y = self.world_size
        x, y = self.image_coordinate(longtitude, latitude)
        dx = abs(round((size / r / math.pi) * im_x))
        dy = abs(round((size / r / math.cos(latitude / 180 * math.pi) / 2 / math.pi) * im_y))
        return self._im[x-dx:x+dx, y-dy:y+dy].mean() / max_light

