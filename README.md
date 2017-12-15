# cloudcoverage
-----
## ABOUT
A python package for estimating cloud coverage and detecting waterspouts! 

_This project was assigned in CSC 380 - Software Engineering at Oswego State College of New York._

Contributors to this project include: 

- Andrew Vadnais
  
- Gage Davidson
  
- Peter Bush
  
- Brandon Copeman

## INSTALLATION

1. To install, first be sure that Python 2.7 is installed. Check this in command line:

        python -V

2. Download the zip of this repository or download from [PyPI](https://pypi.python.org/pypi/cloudcoverage/2.0) to the directory in which you plan to use it and unzip.

3. In the command line, navigate to the cloudcoverage directory

4. Type in command line:

        cloudcoverage setup.py install

5. You may be prompted to install additionally libraries. To do so, you must have [pip](https://pip.pypa.io/en/stable/installing/).

## RECOMMENDED USE

First make sure you import the cloudcoverage module: 

    from cloudcoverage import cloudcoverage
    
Then set up a filepath to the image you want to get the cloud coverage for. This image should contain nothing but the sky. If the image is over a horizon, it should already be cropped at the horizon.
    
See below the various methods you can use with this image.
### ```get_coverage()```

Determines the cloud coverage in your image. If the image was taken during daylight hours, then the coverage will be calculated based on the number of blue pixels in the image. The cloud coverage is 100% - bluepixel%. If the image was taken during the sunrise or sunset hours, we use an experimental function that samples the upper left pixel of the image to see if it is a cloud based on the CloudCascade. If it is, then we step left until a "non-sky" pixel is found. We use the color of this pixel as a base to scan the entire image for similar shades. The cloud coverage is 100% - skypixel%. __*THIS METHOD OF ACQUIRING THE SKY COLOR IS NOT RELIABLE.*__ Therefore, keep in mind when using this function with sunrise and sunset images. __get_coverage() does not support nighttime images as the contrast is too low.__

Arguments:

- ```sky_image_path``` : filepath to image of a sky that has been cropped at the horizon.
    
- ```is_daytime``` : use False if it is night time, sunrise, or sunset. Use True if it is
              during daylight hours. This is used to determine which cloud coverage
              function to call. There is a significantly greater chance of accuracy 
              with images taken during daylight hours. Images at sunrise and sunset 
              are much less likely to be accurate.

Returns:

- new ```Image``` with red overlaid where the clouds were detected

- ```cloud coverage percentage``` as an integer (because the coverage is an estimate, having an
exact floating point representation is ludicrous

Example:

    from cloudcoverage import cloudcoverage
    
    image = <your_image_path>
    coverageimage, coveragepercentage = cloudcoverage.get_coverage(image, True)
    
    coverageimage.show()
    print coverage_percentage
    
This script will show the cloud-detected image in your machine's default image application and print the calculated cloud coverage based on the corresponding image. Note that ```True``` was used in this example which denotes that the image was taken during daylight.

### ```get_waterspouts()```

Detects waterspouts in your image. This function is very good at detecting waterspouts, but unfortunately is also very good at falsely detecting waterspouts. We recommend using caution if you choose to implement automated email notifications in *```get_all()```*.

Arguments:

- ```sky_image_path``` : filepath to image of a sky that has been cropped at the horizon.
    
If waterspouts are detected, returns:

- new ```Image``` with red boxes overlaid on detected waterspouts

- ```True```

If *no* waterspouts are detected, returns:

- ```None```

- ```False```

Example:

    from cloudcoverage import cloudcoverage
    
    image = <your_image_path>
    waterspoutimage, waterspoutsdetected = cloudcoverage.get_waterspouts(image)
    
    if waterspoutsdetected:
        waterspoutimage.show()

    else:
        print "No waterspouts detected."
        
This script will show the waterspout-detected image in your machine's default image application if waterspouts were found.

### ```get_all()```

Calls both ```get_coverage()``` and ```get_waterspouts()``` and automatically sends email notifications to addresses in ```recipients.txt```. __IMPORTANT:__ previously mentioned, false waterspouts are easily detected, so it is recommended that you add only "admins" to the automatic email list and then have the admin check that a waterspout is in the image before forwarding to the list of subscribers.

Arguments:

- ```sky_image_path``` : filepath to image of a sky that has been cropped at the horizon.
    
- ```is_daytime``` : use False if it is night time, sunrise, or sunset. Use True if it is
              during daylight hours. This is used to determine which function to call.
              There is a significantly greater chance of accuracy with images taken during
              daylight hours. Images at sunrise and sunset are much less likely to be accurate.
    
- ```recipients``` : filepath to .txt file containing email addresses of recipients of waterspout alerts.
               Format should be one email address per line with no added punctuation.
    
- ```image_save_to_dir``` : filepath to a directory that a temporary image can be saved to. The image will be saved as
                      "waterspout_temp.jpg" and will be overwritten with the latest waterspout-detected image.
                       This is necessary in order to use the image as an attachment in the email alert.
    
Returns:

- new ```Image``` with red overlaid where the clouds were detected

- cloud coverage percentage as an integer (because the coverage is an estimate, having an
exact floating point representation is ludicrous

- ```True``` if waterspouts detected, ```False``` if not

Example:

    from cloudcoverage import cloudcoverage
    from PIL import Image
    import os
    
    image = <your_image_path>
    
    thisdirectory = os.path.dirname(os.path.abspath(__file__)
    recipients = os.path.join(thisdir, "recipients.txt")
    
    coverageimage, coveragepercentage, waterspoutsdetected = cloudcoverage.get_all(image, True, recipients, thisdirectory)
    
    if coveragepercentage == 0:
        print "No clouds detected! This could mean its clear skies or comlpete overcast."
    else:
        coverageimage.show()
    
    if waterspoutsdetected:
        print "Waterspout(s) detected and email sent!"
    else:
        print "No waterspouts detected."

## HOW IT WORKS

We used opencv to create cascade files (.xml) that are used in the detection process. The original goal for this project was to be able to not only detect clouds, but be able to distinguish between the types of clouds (cumulus, stratus, etc). After extensive testing, this task was deemed impossible due to the ambiguous nature of clouds; they are constantly changing shape. This was true for all types except waterspouts! Waterspouts are distinct, having high contract edges and all waterspouts have similar shape to one another. So, we combined the images we used to train the individual cloud type cascades into one cascade, a generic ```CloudCascade```, and also created a ```WaterspoutCascade```. 

The way cloudcoverage works is by pixel analysis in conjunction with the cascades. If it's daytime, all blue pixels are counted to get the % sky coverage, and the cloud coverage is just 100% - % sky coverage. If it is not daytime, the sky color probably isn't blue! So, a different function is used. First, we run the image through the cloud cascade to detect any clouds. Then we sample the upper left pixel in the image and make sure it hasn't been detected as a cloud. If it has, we sample the next pixel until it is outside of the detected cloud box. Then that pixel's color is taken and the entire image is scanned for shades similar to that pixel. 

*If you can detect clouds, then why do pixel analysis to get cloud coverage?*

Cloud detection using cascades and opencv returns bounding rectangles around clouds and often times the majority of the bounding box's area is sky. It wouldn't make sense to calculate coverage based on those areas. Also, the detection is not completely accurate, again, because clouds are ambiguous and constantly changing. The bounding boxes could just as easily not enclose the entire cloud. This is why during sunrise and sunset hours, the cloud coverage may not be accurate.


## OTHER FUNCTIONS

Additional information on these functions can be found in the source code.

- ```color_printer``` : used to test PIL's HSV naming scheme, makes images of every shade incrementing H,S, and V by 5.

- ```create_blank_HSV``` : creates a blank HSV image with an inputted image's size and inputted background color

- ```create_4x_blank``` : does the same as ```create_blank_HSV``` but image is 2 * width and 2 * height

- ```count_blue_pixels``` : counts all blue pixels in an image

- ```do_testing_vary_q``` : used to test the number of colors to quantize an in image to

- ```do_testing``` : used to test the final algorithms

- ```convert_to_coords``` : converts text file with coordinates to a list of Rectangle objects

- ```wh_to_xy``` : converts 4-tuple (x, y, w, h) to 4-tuple of coordinates ((x1,y1), (x2, y1), (x2, x2), (x2, y1))

- ```overlay_boxes``` : used to overlay rectangles on an image

- ```upper_left``` : used to get the first pixel in an image not contained in cloud bounding box

- ```count_sky_pixels``` : used to count colors similar to an inputted color

- ```get_sky_color``` : experimental function that attempted to find the sky color by scanning the contents of bounding boxes. Too inconsistent to implement in the final function

- ```merge_to_dicts``` : merges two dictionaries into one new dictionary

