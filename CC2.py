from PIL import Image, ImageEnhance, ImageFilter, ImageColor, ImageDraw, ImageFont
import numpy
import colorsys
import os

"""CC2 is the updated version of CC (Cloud Coverage). This program takes in images
and analyzes the pixels to find shades of blue, which represent the sky. The program
then calculates a percentage of cloud coverage based on how much of the image is NOT 
sky pixel
Author: Andrew Vadnais"""
#im.save("/Users/andyvadnais/Desktop/CSC380/cloud.png") # Save the modified pixels as png

#color = ImageColor.getrgb("black")
#print color

#creates an image the size of the input image with a white background



background = (0, 0, 0)

#creates blank image the size of an image parameter and the background of a color parameter
def create_blank(image, background):
    new = Image.new("HSV", (image.width, image.height), background)
    return new

#creates blank image with twice the width and twice the heigh of an image parameter, with the background of a color parameter
def create_4x_blank(image, background):
    new = Image.new("HSV", (2 * image.width, 2 * image.height), background)
    return new

#counts blue pixels in an image and returns the count of blue pixels
def count_blue_pixels(q, newpix):
    sky_count = 0
    h,s,v = 0,0,0
    hsv_sky = []
    for x in range(q.width):
        for y in range(q.height):
            #print "q pixel (", x, ",", y, "): ",q.getpixel((x,y))
            h, s, v = q.getpixel((x, y))
            if (h >= 120 and h < 125 and (s + v > 230)) or\
                (h >= 125 and h < 130 and (s + v > 235)) or\
                (h >= 130 and h < 135 and (s + v > 240)) or\
                (h >= 135 and h < 140 and (s + v > 245)) or\
                (h >= 140 and h < 145 and (s + v > 250)) or\
                (h >= 145 and h < 150 and (s + v > 255)) or\
                (h >= 150 and h < 155 and (s + v > 260)) or\
                (h >= 155 and h < 160 and (s + v > 365)) or\
                (h >= 160 and h < 165 and (s + v > 270)) or\
                (h >= 165 and h < 170 and (s + v > 275)) or\
                (h >= 170 and h < 175 and (s + v > 280)) or\
                (h >= 175 and h < 180 and (s + v > 285)):
                    newpix[x,y] = q.getpixel((x, y))
                    sky_count += 1
    return sky_count

# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype('/Library/Fonts/GillSans.ttc', 12)


def test_images_vary_q(image_from_dir, image_to_dir, qstep, qmax):
    qnum = qstep
    while qnum <= qmax:
        #for every file in given dir
        i = 1 #image counter
        fail = 0 #100% detection counter
        for fileName in os.listdir(image_from_dir):
            #as long as file is .jpg
            if not fileName.endswith(".jpg"):
                continue
                
            print "Processing q" + str(qnum) + " image " + str(i)
    
            #read the image
            im = Image.open(image_from_dir + fileName)
            impix = im.load()
    
            #quantize the image
            q = im.quantize(colors=(qnum), method=1, kmeans=0, palette=None)
    
            #check that image is in a valid mode
            if im.mode == "L":
                continue
        
            #convert images to HSV
            im = im.convert("HSV")
            q = q.convert("HSV")
    
            #create new image to paint pixels to
            new = create_blank(q, (255, 255, 255))
            newpix = new.load()
    
            #create image of twice the width and height of the original
            new4 = create_4x_blank(q, background)
            new4pix = new4.load()
    
            #count blue pixels
            sky_count = count_blue_pixels(q, newpix)
    
            #create new image to write text to
            text = create_blank(q, background)
            draw = ImageDraw.Draw(text)
    
            #calculates total pixels
            totpix = float(q.width) * q.height
    
            #calculates cloud coverage based on blue pixels
            coverage = (1 - float(sky_count / totpix)) * 100
    
            #write cloud coverage to text image
            draw.text((0, (q.height / 2)), "Cloud Coverage:  " + str(coverage) + "%", (0, 0, 255), font)
    
            #for every pixel in the original image
            for x in range(q.width):
                for y in range(q.height):
                    #paint original image to upper left quadrant
                    new4pix[x,y] = im.getpixel((x,y))
            
                    #paint quantized image to upper right quadrant
                    new4pix[(x + q.width), y] = q.getpixel((x,y))
            
                    #paint red detected cloud image to lower left quadrant
                    new4pix[x, (y + q.height)] = new.getpixel((x,y))
            
                    #paint text image to lower right quadrant
                    new4pix[(x + q.width), (y +q.height)] = text.getpixel((x,y))
    
            #check if no "sky" pixels detected and increment fail count
            if coverage == 100:
                fail += 1
    
            #convert image to savable mode and save to corresponding directory
            new4 = new4.convert("RGB")
            new4.save(image_to_dir +"test_images_q" + str(qnum) + "/sky" + str(i) + "test.jpg")
    
            #increment count
            i += 1    
    
        #create text image with number of images and number of "fails", write to directory
        text = create_blank(q, background)
        draw = ImageDraw.Draw(text)
        draw.text((0, (q.height / 2)), "100%  count: " + str(fail) + "\nTotal pics: " + str(i), (0, 0, 255), font)
        text = text.convert("RGB")
        text.save(image_to_dir +"test_images_q" + str(qnum) + "/info.jpg")
        print "Processing q" + str(qnum) + " complete."
        print "Failures:", fail
        print "Total pics:", i
    
        #increment qnum by qstep
        qnum += qstep
            
test_images_vary_q("/Users/andyvadnais/Desktop/f17/Cloud-Coverage-Calculator-master/clouds/",\
"/Users/andyvadnais/Desktop/f17/csc380/CC2_test_cases_loose/", 5, 30)