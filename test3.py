from PIL import Image, ImageEnhance, ImageFilter, ImageColor
import numpy
import colorsys

"""test3 creates images of a solid color and saves them to a directory.
The objective of this program is to manually evaluate the different shades of
colors to discern which are shades of blue, which will be used as sky colors"""

h = 120
s = 10
v = 160
while h <= 180:
    while v < 255:
        while s < 255:
            test = Image.new("HSV", (5, 5), (h, s, v))
            test = test.convert("RGB")
            h = str(h)
            s = str(s)
            v = str(v)
            test.save(("/Users/andyvadnais/Desktop/f17/csc380/test_images/loop7/h" + h + "s" + s + "v" + v +".jpg"))
            h = int(h)
            s = int(s)
            v = int(v)
            s += 5
        s = 10
        test = Image.new("HSV", (5, 5), (h, s, v))
        test = test.convert("RGB")
        h = str(h)
        s = str(s)
        v = str(v)
        test.save(("/Users/andyvadnais/Desktop/f17/csc380/test_images/loop7/h" + h + "s" + s + "v" + v +".jpg"))
        h = int(h)
        s = int(s)
        v = int(v)
        v += 5
    v = 160
    test = Image.new("HSV", (5, 5), (h, s, v))
    test = test.convert("RGB")
    h = str(h)
    s = str(s)
    v = str(v)
    test.save(("/Users/andyvadnais/Desktop/f17/csc380/test_images/loop7/h" + h + "s" + s + "v" + v +".jpg"))
    h = int(h)
    s = int(s)
    v = int(v)
    h += 5