#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-05-21 10:59:50


from PIL import Image

"""
create a mask from an image
"""


class Mask(object):

    def __init__(self, image):
        self.image = image
        self.image_grey = image.convert(mode="L")
        self.size = image.size

    def create_transparent_image(self):
        return self.create_colorful_image("#00000000")

    def create_colorful_image(self, color):
        image = Image.new("RGBA", self.size, color)
        return image

    def get_exclude_white_image(self, tolerance=1):
        threshold = 255 - tolerance
        image = self.create_transparent_image()

        def exclude_white(x):
            if x > threshold:
                return 0
            return 255

        mask = Image.eval(self.image_grey, exclude_white)
        image.paste(self.image, (0,0), mask)
        return image

    def convert_to_single_color(
            self, color, background="#00000000", mode="L"):
        """
        convert the color to a single color image
        params: mode
            L: according the image's brightness
            opacity: according the image's opacity
        """
        bg_image = self.create_colorful_image(background)
        colorful_image = self.create_colorful_image(color)
        if mode == "L":
            bg_image.paste(colorful_image, (0, 0), self.image_grey)
        elif mode == "opacity":
            bg_image.paste(colorful_image, (0, 0), self.image)
        else:
            raise NotImplementedError("the mode can't be recognized")
        return bg_image
