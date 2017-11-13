from PIL import Image, ImageEnhance, ImageFilter, ImageColor, ImageDraw, ImageFont
import numpy
import colorsys

"""CC2 is the updated version of CC (Cloud Coverage). This program takes in images
and analyzes the pixels to find shades of blue, which represent the sky. The program
then calculates a percentage of cloud coverage based on how much of the image is NOT 
sky pixel
Author: Andrew Vadnais"""
#im.save("/Users/andyvadnais/Desktop/CSC380/cloud.png") # Save the modified pixels as png

#color = ImageColor.getrgb("black")
#print color

#creates an image the size of the input image with a white background
def create_blank(q):
    background = (0, 0, 255)
    new = Image.new("HSV", (q.width, q.height), background)
    return new

#counts blue pixels in an image and returns the count of blue pixels
def count_blue_pixels(q):
    sky_count = 0
    h,s,v = 0,0,0
    hsv_sky = []
    for x in range(q.width):
        for y in range(q.height):
            #print "q pixel (", x, ",", y, "): ",q.getpixel((x,y))
            h, s, v = q.getpixel((x, y))
            if (h > 120 and h < 130 and (s + v > 240)) or\
                (h > 130 and h < 140 and (s + v > 245)) or\
                (h > 140 and h < 150 and (s + v > 255)) or\
                (h > 150 and h < 160 and (s + v > 265)) or\
                (h > 160 and h < 170 and (s + v > 275)) or\
                (h > 170 and h < 180 and (s + v > 290)):
                    newpix[x,y] = q.getpixel((x, y))
                    sky_count += 1
    return sky_count


for x in range(8):
    y = str(x + 1)
    q = Image.open("/Users/andyvadnais/Desktop/f17/csc380/sky" + y + ".jpg")
    qpix = q.load()
    print "image size    :",q.size
    q = q.convert("HSV")
    new = create_blank(q)
    newpix = new.load()
    sky_count = count_blue_pixels(q)
    print "image         : sky" + str(x+1)
    #calculates total pixels in image  
    totpix = float(q.width) * q.height
    print "sky pixels    : ", sky_count
    print "total pixels  : ", totpix
    coverage = (1 - float(sky_count / totpix)) * 100
    print "Cloud Coverage: ", coverage, "%\n\n"
    q.show()
    new.show()


