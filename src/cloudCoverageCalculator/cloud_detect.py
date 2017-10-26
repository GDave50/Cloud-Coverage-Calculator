import os, cv2, cloud

OPENCV_WORKSPACE = "C:\\Users\\gaged\\OneDrive\\School\\" + \
        "Cloud Coverage Calculator\\opencv_workspace\\"

CLOUD_CASCADE = cv2.CascadeClassifier(OPENCV_WORKSPACE + "cascades\\cloudsCascade.xml")
CIRRUS_FEATURES = cv2.cvtColor(cv2.imread(OPENCV_WORKSPACE + "cirrusFeat.jpg"), cv2.COLOR_RGB2GRAY)

RECT_THICKNESS = 1
RECT_COLOR = (255, 0, 0)

MIN_SIZE = (50, 50)
MAX_SIZE = (400, 400)
SCALE_FACTOR = 1.5
MIN_NEIGHBORS = 4

def draw_rects(clouds, image):
    for cloud in clouds:
        cv2.rectangle(image, cloud.get_point(),
                cloud.get_opposite_point(), RECT_COLOR, RECT_THICKNESS)

def display_image(image):
    cv2.imshow("Finds", image)
    
    key = 0
    while key != 27:
        key = cv2.waitKey(30) & 0xff
    
    cv2.destroyAllWindows()

def main():
    # for image_path in os.listdir(IMAGES_DIR):
    image = cv2.imread(OPENCV_WORKSPACE + "clouds.jpg")
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    finds = CLOUD_CASCADE.detectMultiScale(gray,
            minSize = MIN_SIZE, maxSize = MAX_SIZE, scaleFactor = SCALE_FACTOR, minNeighbors = MIN_NEIGHBORS)
    
    clouds = []
    
    for x, y, w, h in finds:
        clouds.append(cloud.Cloud(x, y, w, h))
    
    clouds = cloud.trim_cloud_list(clouds)
    clouds = cloud.combine_clouds(clouds)
    clouds = cloud.trim_cloud_list(clouds)
    
    draw_rects(clouds, image)
    
    print(len(clouds), "clouds")
    
    for cloud_ in clouds:
        orb = cv2.ORB_create()
        kp1, des1 = orb.detectAndCompute(gray, None)
        kp2, des2 = orb.detectAndCompute(CIRRUS_FEATURES, None)
        bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck = True)
        matches = bf.match(des1, des2)
        matches = sorted(matches, key = lambda x:x.distance)
        subimage = gray[cloud_.y:(cloud_.y + cloud_.h), cloud_.x:(cloud_.x + cloud_.w)]
        match_image = cv2.drawMatches(subimage, kp1, CIRRUS_FEATURES, kp2,
                matches, flags = 2, outImg = None)
        
        print(len(matches), "matches")
        
        if len(matches) > 0:
            display_image(match_image)

if __name__ == "__main__":
    main()