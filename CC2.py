from PIL import Image, ImageEnhance, ImageFilter, ImageColor, ImageDraw, ImageFont
import numpy
import colorsys
import os
import Rectangle
from shapely.geometry import Polygon, MultiPolygon 
from shapely.ops import cascaded_union
from collections import OrderedDict
mydir = "/Users/andyvadnais/Desktop/f17/csc380/Clouds/"

"""

CC2 is the updated version of CC (Cloud Coverage). This program takes in images
and analyzes the pixels to find shades of blue, which represent the sky. The program
then calculates a percentage of cloud coverage based on how much of the image is NOT 
sky pixel
Author: Andrew Vadnais

"""

#
#   test_colors takes in starting, step, and max values for h, s, and v
#   and iterates through every possible combination of h, s, and v for the 
#   given inputs and saves an image of size (5 x 5) to a given directory.
#   The original purpose of this function was to decipher the PIL convention
#   of naming HSV color values.
#
def test_colors(h0, s0, v0, hstep, sstep, vstep, hmax, smax, vmax, directory):
    h = h0
    s = s0
    v = v0
    while h <= hmax:
        while v <= vmax:
            while s <= smax:
                test = Image.new("HSV", (5, 5), (int(h), int(s), int(v)))
                test = test.convert("RGB")
                test.save(directory + "h" + str(h) + "s" + str(s) + "v" + str(v) +".jpg")
                print "Processing image: H:" + str(h) + " S:" + str(s) + " V:" + str(v)
                s += sstep
            s = s0
            test = Image.new("HSV", (5, 5), (int(h), int(s), int(v)))
            test = test.convert("RGB")
            test.save(directory + "h" + str(h) + "s" + str(s) + "v" + str(v) +".jpg")
            print "Processing image: H:" + str(h) + " S:" + str(s) + " V:" + str(v)
            v += vstep
        v = v0
        test = Image.new("HSV", (5, 5), (int(h), int(s), int(v)))
        test = test.convert("RGB")
        test.save(directory + "h" + str(h) + "s" + str(s) + "v" + str(v) +".jpg")
        print "Processing image: H:" + str(h) + " S:" + str(s) + " V:" + str(v)
        h += hstep

def create_blank_RGB(image, background):
    new = Image.new("RGB", (image.width, image.height), background)
    return new
#creates blank image the size of an image parameter and the background of a color parameter
def create_blank_HSV(image, background):
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
    for x in range(q.width):
        for y in range(q.height):
            print "q pixel (", x, ",", y, "): ",q.getpixel((x,y))
            h, s, v = q.getpixel((x, y))
            if (h >= 120 and h < 125 and (s + v > 250)) or\
                (h >= 125 and h < 130 and (s + v > 255)) or\
                (h >= 130 and h < 135 and (s + v > 270)) or\
                (h >= 135 and h < 140 and (s + v > 275)) or\
                (h >= 140 and h < 145 and (s + v > 280)) or\
                (h >= 145 and h < 150 and (s + v > 285)) or\
                (h >= 150 and h < 155 and (s + v > 305)) or\
                (h >= 155 and h < 160 and (s + v > 310)) or\
                (h >= 160 and h < 165 and (s + v > 325)) or\
                (h >= 165 and h < 170 and (s + v > 330)) or\
                (h >= 170 and h < 175 and (s + v > 335)) or\
                (h >= 175 and h < 180 and (s + v > 340)):
                    newpix[x,y] = q.getpixel((x, y))
                    sky_count += 1
    return sky_count

            


# font = ImageFont.truetype(<font-file>, <font-size>)
font = ImageFont.truetype('/Library/Fonts/GillSans.ttc', 40)

def calculate_coverage(imagePath, skycolor):
    new = create_blank_HSV(openIm(im), (255,255,255))
    newpix = new.load()
    new4 = create_4x_blank(im, (0,0,0))
    new4pix = new4.load()
    
def openIm(filePath):
    return Image.open(filePath)

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
            new = create_blank_HSV(q, (255, 255, 255))
            newpix = new.load()
    
            #create image of twice the width and height of the original
            new4 = create_4x_blank(q, background)
            new4pix = new4.load()
    
            #count blue pixels
            sky_count = count_blue_pixels(q, newpix)
    
            #create new image to write text to
            text = create_blank_HSV(q, background)
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
        text = create_blank_HSV(q, background)
        draw = ImageDraw.Draw(text)
        draw.text((0, (q.height / 2)), "100%  count: " + str(fail) + "\nTotal pics: " + str(i), (0, 0, 255), font)
        text = text.convert("RGB")
        text.save(image_to_dir +"test_images_q" + str(qnum) + "/info.jpg")
        print "Processing q" + str(qnum) + " complete."
        print "Failures:", fail
        print "Total pics:", (i-1)
    
        #increment qnum by qstep
        qnum += qstep
            
def doTesting(image_from_dir, image_to_dir):
    background = (0,0,0)
    #for every file in given dir
    fail = 0
    i = 1 #image counter
    for fileName in os.listdir(image_from_dir):
        #as long as file is .jpg
        if not fileName.endswith(".jpg"):
            continue
                
        print "Processing image " + str(i)
    
        #read the image
        im = Image.open(image_from_dir + fileName)
        txtfile = image_from_dir + fileName.strip(".jpg") + ".txt"
        impix = im.load()
    
        q = im.quantize(colors=20, method=1, kmeans=0, palette=None)
        #check that image is in a valid mode
        if im.mode == "L":
            continue
        
        #convert images to HSV
        im = im.convert("HSV")
        q = q.convert("HSV")
       
        
        #create new image to paint pixels to
        new = create_blank_HSV(im, (255, 255, 255))
        newpix = new.load()
    
        #create image of twice the width and height of the original
        new4 = create_4x_blank(im, background)
        new4pix = new4.load()
    
        #call function to covert textfile to coordinate dictionary
        rects = ConvertToCoords(txtfile)
        z = OverlayBoxes(q, FromWHtoXY(rects), fill=None, outline=ImageColor.getrgb("pink"))
        boxIm = OverlayBoxes(im, FromWHtoXY(rects), fill=None, outline=ImageColor.getrgb("pink"))
        
        #call function to get sky color
        print "Box_Contents started"
        skycolors = box_contents_minority(q, rects)
        print "Box_Contents complete"
        
        #count sky pixels
        sky_count = count_sky_pixels(q, skycolors, newpix)
        #create new image to write text to
        text = create_blank_HSV(im, background)
        draw = ImageDraw.Draw(text)
    
        #calculates total pixels
        totpix = float(im.width) * im.height
    
        #calculates cloud coverage based on blue pixels
        coverage = (1 - float(sky_count / totpix)) * 100
    
        #write cloud coverage to text image
        draw.text((0, (im.height / 2)), "Cloud Coverage:  " + str(coverage) + "%", (0, 0, 255), font)
    
        #for every pixel in the original image
        for x in range(im.width):
            for y in range(im.height):
                #paint original image to upper left quadrant
                new4pix[x,y] = im.getpixel((x,y))
            
                #paint quantized image to upper right quadrant
                new4pix[(x + im.width), y] = boxIm.getpixel((x,y))
            
                #paint red detected cloud image to lower left quadrant
                new4pix[x, (y + im.height)] = new.getpixel((x,y))
            
                #paint text image to lower right quadrant
                new4pix[(x + im.width), (y +im.height)] = z.getpixel((x,y))
    
        #check if no "sky" pixels detected and increment fail count
        if coverage == 100:
            fail += 1
    
        #convert image to savable mode and save to corresponding directory
        new4 = new4.convert("RGB")
        new4.save(image_to_dir +"test_images_" + str(i) + ".jpg")
    
        #increment count
        i += 1    
    
    #create text image with number of images and number of "fails", write to directory
    text = create_blank_HSV(im, background)
    draw = ImageDraw.Draw(text)
    draw.text((0, (im.height / 2)), "100%  count: " + str(fail) + "\nTotal pics: " + str(i), (0, 0, 255), font)
    text = text.convert("RGB")
    text.save(image_to_dir + "test_images_info.jpg")
    print "Failures:", fail
    print "Total pics:", (i-1)

            
def ConvertToCoords(textFile):
    txt = open(textFile, 'r')
    c = txt.read().splitlines()
    rects = {}
    for i in range(len(c)):
        z = c[i]
        z = z.strip("[]")
        z = z.split(",")
        x = int(z[0])
        y = int(z[1])
        w = int(z[2])
        h = int(z[3])
        rect = Rectangle.Rectangle(x,y,w,h)
        rects['rect ' + str(i)] = rect

    return rects

def FromWHtoXY(rects):
    newRects = {}
    for key in rects:
        x = rects[key].x
        y = rects[key].y
        w = rects[key].w
        h = rects[key].h
        x0,y0 = rects[key].GetPoint()
        x1,y1 = rects[key].GetOppositePoint()
        box = [(x0, y0), (x0, y1), (x1, y1), (x1, y0)]
        newRects[key] = box
           
    return newRects

def Overlaps(rects):
    newCoords = {}
    for key in rects:
        pt1 = rects[key][0]
        pt2 = rects[key][1]
        pt3 = rects[key][2]
        pt4 = rects[key][3]
        for key2 in rects:
            npt1 = rects[key2][0]
            npt2 = rects[key2][1]
            npt3 = rects[key2][2]
            npt4 = rects[key2][3]
            poly1 = Polygon([pt1,pt2,pt3,pt4])
            poly2 = Polygon([npt1,npt2,npt3,npt4])              
            if (not poly1.intersects(poly2)) and not poly1.within(poly2):
                newCoords['poly ' + str(key)] = rects[key]   
            elif poly1.intersects(poly2):
                newCoords['poly ' + str(key)] = list(set(list(poly1.exterior.coords) + list(poly2.exterior.coords)))
    return newCoords

#
#   takes in an image, a dictionary with "box" keys and (x,y) coordinate values and overlays boxes onto the iamge at the
#   dictionariy's coordinates with specified fill and outline colors
#
def OverlayBoxes(im, coordinates, fill, outline):
    copy = im.copy()
    draw = ImageDraw.Draw(copy)
    for key in coordinates:
        #print coordinates[key][0]
        draw.polygon(coordinates[key], outline=outline)
    return copy
        
    

def MakePolyFromBoxes(im, boxim):
    #copy3 is original image with red dots at box corners and green dots at 4 way intersections
    #copy2 is original image with lines connecting intersections
    #copy is original image with red bounding boxes around clouds and yellow dots at corners and intersections 
    copy3 = im.copy()
    copy3pix = copy3.load()
    copy = boxim.copy()
    pix = boxim.load()
    copypix = copy.load()
    draw = ImageDraw.Draw(copy)
    intersections = []
    for x in range(boxim.width - 1):
        for y in range(boxim.height - 1):
            if x!=0 and y!=0:
                if pix[x, y] == (255, 0, 0):
                    if (pix[x+1, y] == (255, 0, 0) or\
                    pix[x-1, y] == (255, 0, 0)) and\
                    (pix[x, y+1] == (255, 0, 0) or\
                    pix[x, y-1] == (255, 0, 0)):
                        intersections.append((x,y))
                        copypix[x,y] = ImageColor.getrgb("yellow")
                        copy3pix[x,y] = ImageColor.getrgb("red")
                    if (pix[x+1, y] == (255, 0, 0) and\
                    pix[x-1, y] == (255, 0, 0) and\
                    (pix[x, y+1] == (255, 0, 0) and\
                    pix[x, y-1] == (255, 0, 0))):
                        copy3pix[x,y] = ImageColor.getrgb("green")
                        intersections.remove((x,y))
                                      
    copy2 = im.copy()
    draw2 = ImageDraw.Draw(copy2)
    draw2.line(intersections, ImageColor.getrgb("yellow"), 1)
    copy.show()
    new = Image.new("RGB", (boxim.width, boxim.height), ImageColor.getrgb("white"))
    newpix = new.load()

    return intersections
    
##non functional
def TraceOutline(orig, im):
    #create copy of original image to trace to
    copy = orig.copy()
    copypix = copy.load()
    pix = im.load()
    red = ImageColor.getrgb("red")
    x = 0
    y = 0
    lastStep = ''
    while y <= im.height:
        if pix[x,y] == red:
            #right step
            if (pix[x + 1 , y] == red) and lastStep != 'l' and copypix[x + 1 , y] != red:
                copypix[x + 1 , y] = pix[x + 1 , y]
                x += 1
                print "Right Step"
                print "(" + str(x) + "," + str(y) + ")"
                lastStep = 'r'              
            #down step     
            elif pix[x , y + 1] == red and lastStep != 'u' and copypix[x , y + 1] != red:
                copypix[x , y + 1] = pix[x , y + 1]
                y += 1
                print "Down Step"
                print "(" + str(x) + "," + str(y) + ")"
                lastStep = 'd'
            #up step
            elif pix[x , y - 1] == red and lastStep != 'd' and copypix[x , y - 1] != red:
                print "ENTERED UP STEP"
                copypix[x , y - 1] = pix[x, y - 1]
                y -= 1
                print "Up Step"
                print "(" + str(x) + "," + str(y) + ")"
                lastStep = 'u'
            #left step
            elif pix[x - 1, y] == red and lastStep != 'r' and copypix[x - 1 , y] != red:
                copypix[x - 1, y] = pix[x - 1, y]
                x -= 1
                print "Left step"
                print "(" + str(x) + "," + str(y) + ")"
                lastStep = 'l'
            copy.save("/Users/andyvadnais/Desktop/f17/csc380/trace.jpg")

        else:
            x += 1
            print "Default right step"
            print "(" + str(x) + "," + str(y) + ")"
            
        if x >= im.width:
            x = 0
            y += 1

    return copy
    
    
def upper_left(im, rects):
    pix = im.load()
    skycolor = ""
    for x in range(im.width):
        for y in range(im.height):
            for key in rects:
                if not rects[key].Contains(x ,y):
                    skycolor = pix[x,y]
                    pix[x,y] = ImageColor.getrgb("red")
                break
            break
        break
                    
    print "image size: (" + str(im.width) + "," + str(im.height) + ")"
    print "x,y: " + str(x) + " " + str(y)
    return skycolor
 
 
def count_colors(im, colors, newpix):
    count = 0
    for y in range(im.height):
        for x in range(im.width):
            for color in colors:
                if im.getpixel((x,y)) == colors[color]:
                    newpix[x,y] = im.getpixel((x,y))
                    count += 1
                    break
    return count


def count_sky_pixels(im, skycolor, newpix):
    sky_count = 0
    for y in (range(im.height-1)):
        for x in (range(im.width-1)):
            h, s, v = im.getpixel((x,y))
            for key in skycolor:
                if (h,s,v) == skycolor[key]:
                    newpix[x,y] = im.getpixel((x,y))
                    sky_count +=1
                    break
    
    return sky_count
    
#
#   get_sky_color goes through each bounding box on an image and finds colors that are similar to each other.
#   These colors are considered to be sky colors, since the sky is a gradient, versus clouds that have high contrast.
#
def get_sky_color(im, rects):
    firstpix = {}
    i = y = x = 0
    for key in rects:
        h0, s0, v0 = im.getpixel((rects["rect " + str(i)].x, rects["rect " + str(i)].y))
        while y < (rects[key].y + rects[key].h):
            while x < (rects[key].x + rects[key].w):
                scount = 0
                h,s,v = im.getpixel((x,y))
                diffH = abs(h - h0)
                diffSV = abs((s + v) - (s0 + v0))
                if diffH > 10 and diffH <= 20 and diffSV <= 70 or\
                diffH > 20 and diffH <= 30 and diffSV <= 60 or\
                diffH > 30 and diffH <= 40 and diffSV <= 50 or\
                diffH > 40 and diffH <= 50 and diffSV <= 40 or\
                diffH > 50 and diffH <= 60 and diffSV <= 30 or\
                diffH > 60 and diffH <= 70 and diffSV <= 20 or\
                diffH > 70 and diffH <= 80 and diffSV <= 10:
                    scount += 1
                x+=1
            y+=1
        if rects[key].w * rects[key].h - scount > scount:
            firstpix["Sky Color " + str(len(firstpix))] = (h0, s0, v0)
        i += 1
    
    return firstpix
    


doTesting("/Users/andyvadnais/Desktop/f17/csc380/Clouds/",\
"/Users/andyvadnais/Desktop/f17/csc380/tests/test3/")