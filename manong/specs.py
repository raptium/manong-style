# -*- coding:utf-8 -*-
"""
This module defines the Specification
for the fabric patterns.
"""
import collections
import numpy as np
from PIL import Image, ImageColor


class Element(object):
    def __init__(self, color_or_element, repeat=1):
        if isinstance(color_or_element, Element):
            self.element = color_or_element
            self.color = None
        else:
            self.element = None
            self.color = np.array(ImageColor.getrgb(color_or_element))
        self.repeat = repeat

    def __len__(self):
        if self.color is not None:
            return self.repeat
        return len(self.element) * self.repeat

    def to_array(self):
        if self.color is not None:
            return np.tile(self.color, (self.repeat, 1))
        else:
            return np.repeat(self.element.to_array(), self.repeat)


class Series(object):
    def __init__(self, elements):
        self.elements = elements

    def __len__(self):
        return sum(map(len, self.elements))

    def to_array(self, shift=0):
        ret = np.concatenate([e.to_array() for e in self.elements])
        return np.roll(ret, shift * 3)


class Pattern(object):
    def __init__(self, vertical, horizontal, line_width=2):
        """
        """
        if horizontal is None:
            horizontal = vertical
        if not isinstance(vertical, Series):
            vertical = Series(vertical)
        if not isinstance(horizontal, Series):
            horizontal = Series(horizontal)
        self.vertical = vertical
        self.horizontal = horizontal
        self.line_width = line_width

    def draw(self, canvas_w, canvas_h):
        h = len(self.vertical)
        w = len(self.horizontal)
        data = np.zeros((w * 4, h * 4, 3), 'uint8')
        for x in range(w):
            for shift in range(4):
                values = self.vertical.to_array()
                y = x * 4 + shift
                data[shift::4, y] = values
                data[(shift + 1) % 4::4, y] = values
        for y in range(h):
            for shift in range(4):
                values = self.horizontal.to_array()
                x = (y * 4 + shift - 1) % (4 * h)
                data[x, shift::4] = values
                data[x, (shift + 1) % 4::4] = values
        data = np.tile(data, [4, 4, 1])
        image = Image.fromarray(data, 'RGB')
        ratio = self.line_width * 1.0 / 2
        if ratio != 1:
            w, h = image.size
            image = image.resize((int(w * ratio), int(h * ratio)),
                                 Image.ANTIALIAS)
        return image
