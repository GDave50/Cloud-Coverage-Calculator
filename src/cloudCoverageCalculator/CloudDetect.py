import os

import cv2

def main():
    PROJECT_DIR = "C:\\Users\\gaged\\OneDrive\\School\\Cloud Coverage Calculator\\"
    OPENCV_WORKSPACE = PROJECT_DIR + "opencv_workspace\\"
    
    print("Loading cascade")
    #cirrus_cascade = cv2.CascadeClassifier(OPENCV_WORKSPACE + "clouds\\cirrus\\cascade\\cascade.xml")
    cumulus_cascade = cv2.CascadeClassifier(OPENCV_WORKSPACE + "clouds\\cumulus\\cascade\\cascade.xml")
    #stratus_cascade = cv2.CascadeClassifier(OPENCV_WORKSPACE + "clouds\\stratus\\cascade\\cascade.xml")
    
    #IMAGE_PATH = OPENCV_WORKSPACE + "clouds - Copy\\cumulus\\image721.jpg"
    IMAGE_PATH = "C:\\Users\\gaged\\Downloads\\cumulus.jpg"
    
    image = cv2.imread(IMAGE_PATH)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    print("Detecting clouds")
    clouds = cumulus_cascade.detectMultiScale(gray)
    
    print("-----")
    
    for (x, y, w, h) in clouds:
        print(x, y, w, h)
        cv2.rectangle(image, (x, y), (x+w, y+h), (255, 0, 0), 2)
    
    cv2.imshow("image", image)
    
    key = 0
    while key != 27:
        key = cv2.waitKey(30) & 0xff
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
