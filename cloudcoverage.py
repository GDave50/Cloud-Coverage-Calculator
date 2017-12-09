from PIL import Image, ImageColor, ImageDraw, ImageFont
import numpy
import colorsys
import os
import Rectangle
from shapely.geometry import Polygon

def get_all(skyimage, isDaytime):
    newpix = skyimage.load()
    if isDaytime:
        count = count_blue_pixels(skyimage, newpix)
    else:
        #TODO RUN THROUGH CASCADE & GET BOUNDING RECTANGLES
        #rects = list of rects returned from image run through clouds cascade
        q = im.quantize(colors=15, method=1)
        sky = upper_left(q, rects)
        count = count_sky_pixels(q, im, sky, newpix)
    
    #calculate cloud coverage
    coverage = (1 - float(count / (skyimage.width * skyimage.height))) * 100
    
    return skyimage, coverage

#########TESTING get_all#############
#insert your filepath to test image
im = Image.open("/Users/andyvadnais/Desktop/f17/csc380/sky4.jpg")
get_all(im, True)
#show result
im.show()


def color_printer(h0, s0, v0, hstep, sstep, vstep, hmax, smax, vmax, directory):
    
    """takes in starting, step, and max values for h, s, and v
    and iterates through every possible combination of h, s, and v for the 
    given inputs and saves an image of size (5 x 5) to a given directory.
    The original purpose of this function was to decipher the PIL convention
    of naming HSV color values.
    
    Arguments
    -
    h0          - hue value to start with
    
    s0          - saturation value to start with
    
    v0          - value (brightness) value to start with
    
    hstep       - step by which to increment hue
    
    sstep       - step by which to increment saturation
    
    vstep       - step by which to increment value 
    
    hmax        - hue value to stop at
    
    smax        - saturation value to stop at
    
    vmax        - value value to stop at
    
    directory   - filepath to directory to save images to
    
    """
    
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

def create_blank_HSV(image, background):
    """ Returns a blank HSV mode image
    
    Arguments
    -
    image       - an image opened with PIL Image, the size of this image
                is used to determine the size of the blank image. This fuction
                is set up with this convention because it is most useful for
                this program to create blank images the same size as an original.
    
    background  - 3-tuple HSV color (h, s, v)
    """
    new = Image.new("HSV", (image.width, image.height), background)
    return new

def create_4x_blank(image, background):
    """ Returns a blank HSV mode image of size 2 * input image width and 2 * input image height
    
    Arguments
    -
    image       - an image opened with PIL Image, the size of this image
                is used to determine the size of the blank image. This fuction
                is set up with this convention because it is most useful for
                this program to create blank images the same size as an original.
    
    background  - 3-tuple HSV color (h, s, v)
    """
    new = Image.new("HSV", (2 * image.width, 2 * image.height), background)
    return new

def count_blue_pixels(image, newpix):
    """ Counts blue shaded pixels
    
    Arguments
    -
    image       - an image opened with PIL Image, the size of this image
                is used to determine the size of the blank image. 
    
    newpix      - allows manipulation of an image. This variable should be 
                created by opening an image with PIL Image and then using the 
                Image.load() function to allow for pixel manipulation
    """
    sky_count = 0
    h,s,v = 0,0,0
    for x in range(image.width):
        for y in range(image.height):
            h, s, v = image.getpixel((x, y))
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
                    newpix[x,y] = image.getpixel((x, y))
                    sky_count += 1
    return sky_count

def do_testing_vary_q(image_from_dir, image_to_dir, qstep, qmax):
    """Saves test images with varying quantization to specified directory
    
    Arguments
    -
    image_from_dir      - filepath to directory with images
    
    image_to_dir        - filepath to directory to save test images to
    
    qstep               - the step at which the quantization of colors should be incremented
                        this allows the programmer to test which quantization value yields the 
                        best results
    
    qmax                - the ending quantization value to stop testing at
    """
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

def do_testing(image_from_dir, image_to_dir):
    """Saves test images to specified directory
    
    Arguments
    -
    image_from_dir      - filepath to directory with images
    
    image_to_dir        - filepath to directory to save test images to
    """
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
    
        q = im.quantize(colors=15, method=1, kmeans=0, palette=None)
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
        skycolor = upper_left(q, rects)
        
        #count sky pixels
        sky_count = count_blue_pixels(q, newpix)
        
        #create new image to write text to
        text = create_blank_HSV(im, background)
        draw = ImageDraw.Draw(text)
    
        #calculates total pixels
        totpix = float(im.width) * im.height
    
        #calculates cloud coverage based on blue pixels
        coverage = (1 - float(sky_count / totpix)) * 100
    
        #for every pixel in the original image
        for x in range(im.width):
            for y in range(im.height):
                #paint original image to upper left quadrant
                new4pix[x,y] = im.getpixel((x,y))
            
                #paint quantized image to upper right quadrant
                new4pix[(x + im.width), y] = boxIm.getpixel((x,y))
            
                #paint red detected cloud image to lower left quadrant
                new4pix[x, (y + im.height)] = new.getpixel((x,y))
            
                #paint quantized image with overlaid boxes to lower right
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
    print "Failures:", fail
    print "Total pics:", (i-1)

def ConvertToCoords(textfile):
    """Parses a text file with format [x, y, w, h] on each line to a dictionary with Rectangle objects
    
    Arguments
    -
    textfile    - each line contains the starting x and y values (coordinate), width, and height of a single rectangle
    """
    txt = open(textfile, 'r')
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
    """ Converts a dictionary of Rectangle objects to a dictionary of 4-tuples
    which are (x,y) coordinates of each corner each rectangle
    
    Arguments
    -
    rects       - dictionary of Rectangle objects
    """
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

def OverlayBoxes(im, coordinates, fill, outline):
    """ Returns a new image with boxed overlaid on the input image
    
    Arguments
    -
    im          - image of sky
    
    coordinates - dictionary of 4-tuples consisting of (x,y) coordinates of each rectangle
    
    fill        - RGB color value (r, g, b) to fill the boxes
    
    outline     - RGB color value (r, g, b) to outline the boxes
    """
    copy = im.copy()
    draw = ImageDraw.Draw(copy)
    for key in coordinates:
        #print coordinates[key][0]
        draw.polygon(coordinates[key], outline=outline)
    return copy

def upper_left(im, rects):
    """Returns the color of the first pixel not contained in a bounding box
        If no bounding boxes, returns None
    
    Arguments
    -
    im      - sky image that corresponds to rects
    
    rects   - dictionary of Rectangle objects corresponding to im
    """
    pix = im.load()
    skycolor = ""
    for x in range(im.width):
        for y in range(im.height):
            for key in rects:
                if not rects[key].Contains(x ,y):
                    skycolor = im.getpixel((x,y))
                    return     
    return None

def count_sky_pixels(q, im, skycolor, newpix):
    """Counts sky colored pixels in an image. Paints all sky colored pixels to
    Image.load() variable. Returns sky pixel count
    
    Arguments
    -
    q           - sky image that has been quantized
    
    im          - original sky image not quantized
    
    skycolor    - either a dictionary of sky colors or a single sky color in (h,s,v) format.
                If skycolor is a dictionary, then the function counts all exact color matches.
                If skycolor is a single color, then the function counts all colors within a   
                range of values. Ample testing was conducted to maximize the accurate of the range of values.
                This is tricky because to the naked eye, one can tell the range of colors that is the sky. 
                When using HSV, it is somewhat arbitrary when deciding what range of values should be considered
                similar enough to also be sky
    
    newpix      - Image.load() variable

    """
    sky_count = 0
    for y in (range(q.height)):
        for x in (range(q.width)):
            #if skycolor is a dictionary
            if type(skycolor) == 'dict':
                #iterate through skycolor dict
                for key in skycolor:
                    #compare each pixel to skycolor
                    h, s, v = q.getpixel((x,y))
                    if (h,s,v) == skycolor[key]:
                        #if theres a match, set newpix to current im pixel, increment skycount
                        newpix[x,y] = im.getpixel((x,y))
                        sky_count +=1
                        
            #skycolor is not a dictionary
            else:
                h,s,v = skycolor
                h0,s0,v0 = q.getpixel((x,y))
                diffH = abs(h - h0)
                diffSV = abs((s + v) - (s0 + v0))
                #check is pixel is within range of original color
            	if diffH <= 10 and diffSV <= 80 or\
                diffH > 10 and diffH <= 20 and diffSV <= 70 or\
                diffH > 20 and diffH <= 30 and diffSV <= 60 or\
                diffH > 30 and diffH <= 40 and diffSV <= 50 or\
                diffH > 40 and diffH <= 50 and diffSV <= 40 or\
                diffH > 50 and diffH <= 60 and diffSV <= 30 or\
                diffH > 60 and diffH <= 70 and diffSV <= 20 or\
                diffH > 70 and diffH <= 80 and diffSV <= 10:
                    newpix[x,y] = im.getpixel((x,y))
                    sky_count +=1
    
    return sky_count

def get_sky_color(im, rects):
    """EXPERIMENTAL FUNCTION
    
    Iterates through each bounding box on an image and finds colors that are similar to each other. If the 
    less than half of the contents of the bounding box match the similar colors, then those colors are considered to be sky,
    else the colors are removed from the similar color dictionary.
    Returns the similar colors
    """
    skypix = {}
    simpix = {}
    i = y = x = 0
    for key in rects:
        h0, s0, v0 = im.getpixel(((rects["rect " + str(i)].x +rects["rect " + str(i)].w)/2, (rects["rect " + str(i)].y+ rects["rect " + str(i)].h)/2))
        while y < (rects[key].y + rects[key].h):
            while x < (rects[key].x + rects[key].w):
                scount = 0
                h,s,v = im.getpixel((x,y))
                diffH = abs(h - h0)
                diffSV = abs((s + v) - (s0 + v0))
            	if diffH <= 10 and diffSV <= 80 or\
                diffH > 10 and diffH <= 20 and diffSV <= 70 or\
                diffH > 20 and diffH <= 30 and diffSV <= 60 or\
                diffH > 30 and diffH <= 40 and diffSV <= 50 or\
                diffH > 40 and diffH <= 50 and diffSV <= 40 or\
                diffH > 50 and diffH <= 60 and diffSV <= 30 or\
                diffH > 60 and diffH <= 70 and diffSV <= 20 or\
                diffH > 70 and diffH <= 80 and diffSV <= 10:
                    scount += 1
                    simpix[str(i) + "Color "] = (h0, s0, v0)
                    
                x+=1
            y+=1
        if rects[key].w * rects[key].h - scount > scount:
            skypix = merge_two_dicts(skypix, simpix)
        i += 1
    
    return skypix

def merge_two_dicts(x,y):
    """Combines two dictionaries into a single, new dictionary
    
    Arguments
    -
    x   - a dictionary
    
    y   - a dictionary
    """
    z = x.copy()
    z.update(y)
    return z