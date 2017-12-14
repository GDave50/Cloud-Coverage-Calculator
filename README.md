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

2. Download the zip of this repository to the directory in which you plan to use it and unzip.

3. In the command line, navigate to the cloudcoverage directory

4. Type in command line:

        cloudcoverage setup.py install

5. You may be prompted to install additionally libraries. To do so, you must have [pip](https://pip.pypa.io/en/stable/installing/).

## RECOMMENDED USE

First make sure your header has: 

    from cloudcoverage import cloudcoverage
    
Then set up a filepath to the image you want to get the cloud coverage for. This image should contain nothing but the sky. If the image is over a horizon, it should already be cropped at the horizon.
    
See below the various methods you can use this image with.
### get_coverage()

Determines the cloud coverage in your image. If the image was taken during daylight hours, then the coverage will be caluculated based on the number of blue pixels in the image. The cloud coverage is 100% - bluepixel%. If the image was taken during the sunrise or sunset hours, we use an experimental function that sampled the upper left pixel of the image to see if it is a cloud based on the CloudCascade. If it is, then we step left until a "non-sky" pixel is found. We then use the color of this pixel as a base to scan the entire image for similar shades. The cloud coverage is 100% - skypixel%. __*THIS METHOD OF ACQUIRING THE SKY COLOR IS NOT RELIABLE.*__ Therefore, keep in mind when using this function with sunrise and sunset images. __get_coverage() does not support nighttime images as the contrast is too low.__

Arguments:

- sky_image_path: filepath to image of a sky that has been cropped at the horizon.
    
- is_daytime: use False if it is night time, sunrise, or sunset. Use True if it is
              during daylight hours. This is used to determine which cloud coverage
              function to call. There is a significantly greater chance of accuracy 
              with images taken during daylight hours. Images at sunrise and sunset 
              are much less likely to be accurate.

Returns:

- new Image with red overlaid where the clouds were detected

- cloud coverage percentage as an integer (because the coverage is an estimate, having an
exact floating point representation is ludicrous

Example:

    from cloudcoverage import cloudcoverage
    from PIL import Image
    
    path = <your_image_path>
    coverage_image, coverage_percentage = cloudcoverage.get_coverage(image, True)
    
    coverage_image.show()
    print coverage_percentage
    
This script will show the cloud-detected image in your machine's default image application and print the calculated cloud coverage based on the corresponding image. Note that "True" was used in this example which denotes that the image was taken during daylight.

### get_waterspouts()

Detects waterspouts in your image. This function is very good at detecting waterspouts, but unfortunately is also very good at falsely detecting waterspouts. We recommend using caution if you choose to implement automated email notifications in *get_all()*.

Arguments:

- sky_image_path: filepath to image of a sky that has been cropped at the horizon.
    
If waterspouts are detected, returns:

- new Image with red boxes overlaid on detected waterspouts

- True

If *no* waterspouts are detected, returns:

- None

- False

Example:

    from cloudcoverage import cloudcoverage
    from PIL import Image
    
    path = <your_image_path>
    waterspout_image, waterspouts_detected = cloudcoverage.get_waterspouts(image)
    
    if waterspouts_detected:
        waterspout_image.show()

    else:
        print "No waterspouts detected."
        
This script will show the waterspout-detected image in your machine's default image application if waterspouts were found.

