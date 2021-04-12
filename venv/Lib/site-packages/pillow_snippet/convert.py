#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
# Xiang Wang @ 2019-05-10 16:47:20


import io

from PIL import Image, ImageColor, ImageDraw
import requests


def convert_image(from_image, to_image, background, frontcolor):
    # TODO add comment
    raise Exception("please complete the mask function first")
    img = Image.open(from_image)
    image_size = img.size
    img = img.resize(image_size)
    img = img.convert(mode="L")
    img = Image.eval(img, exclude_black_and_white)
    result = Image.new("RGBA", image_size, background)
    yellow = Image.new("RGBA", image_size, frontcolor)
    result.paste(yellow, (0, 0), mask=img)
    result.save(to_image)


def circle_image(from_image):
    """
    create the circle image from a square ImageClass
    """
    image_size = from_image.size
    assert image_size[0] == image_size[1], "The image has different dimension"
    image = Image.new("RGBA", image_size, "#00000000")
    draw = ImageDraw.Draw(image)
    draw.chord(
        ((0,0), image_size),
        0, 360,
        outline="#FF0000",
        fill="#00FF00",
        width=3,)
    image.paste(from_image, (0,0), image)
    return image
