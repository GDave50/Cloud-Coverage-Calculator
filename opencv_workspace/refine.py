import os, cv2

OPENCV_WORKSPACE = "C:\\Users\\gaged\\OneDrive\\School\\" + \
        "Cloud Coverage Calculator\\opencv_workspace\\"

RAW_POS_DIR = OPENCV_WORKSPACE + "raw\\pos\\"
RAW_NEG_DIR = OPENCV_WORKSPACE + "raw\\neg\\"
REFINED_DIR = OPENCV_WORKSPACE + "refined\\"

RESIZE_DIM = 40
POS_INFO_FORMAT = "%s 1 0 0 %d %d\n"

def write_file(file_path, text):
    print("Saving file")
    file = open(file_path, "w+")
    file.write(text)
    file.close()

def load_grayscale_image(image_path):
    image = cv2.imread(image_path)
    return cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def refine_clouds():
    print("\nStarting refinement process for clouds")
    
    clouds_types = ["cirrus", "cumulus", "stratus"]
    
    refined_dir = REFINED_DIR + "clouds\\"
    info = ""
    
    for i in range(0, len(clouds_types)):
        print("Refining", clouds_types[i])
        
        raw_dir = RAW_POS_DIR + clouds_types[i] + "\\"
        
        image_names = os.listdir(raw_dir)
        
        for j in range(0, len(image_names)):
            image_path = raw_dir + image_names[j]
            gray = load_grayscale_image(image_path)
            resized_image = cv2.resize(gray,
                    (RESIZE_DIM, RESIZE_DIM), interpolation = cv2.INTER_AREA)
            
            new_image_name = "%s%d.jpg" % (clouds_types[i], j)
            new_image_path = refined_dir + new_image_name
            
            cv2.imwrite(new_image_path, resized_image)
            
            info += POS_INFO_FORMAT % \
                    ("clouds\\" + new_image_name, RESIZE_DIM, RESIZE_DIM)
    
    info_path = REFINED_DIR + "clouds_info.data"
    write_file(info_path, info)
    
    print("Done refining")

def refine_waterspout():
    print("\nStarting refinement process for waterspout")
    
    raw_dir = RAW_POS_DIR + "waterspout\\"
    refined_dir = REFINED_DIR + "waterspout\\"
    
    info = ""
    image_names = os.listdir(raw_dir)
    
    for i in range(0, len(image_names)):
        image_path = raw_dir + image_names[i]
        gray = load_grayscale_image(image_path)
        resized_image = cv2.resize(gray,
                (RESIZE_DIM, RESIZE_DIM), interpolation = cv2.INTER_AREA)
        
        new_image_name = "waterspout%d.jpg" % (i)
        new_image_path = refined_dir + new_image_name
        
        cv2.imwrite(new_image_path, resized_image)
        
        info += POS_INFO_FORMAT % \
                ("waterspout\\" + new_image_name, RESIZE_DIM, RESIZE_DIM)
    
    info_path = REFINED_DIR + "waterspout_info.data"
    write_file(info_path, info)
    
    print("Done refining")

def refine_neg():
    print("\nStarting refinement process for negatives")
    
    info = ""
    image_names = os.listdir(RAW_NEG_DIR)
    
    for i in range(0, len(image_names)):
        image_path = RAW_NEG_DIR + image_names[i]
        gray = load_grayscale_image(image_path)
        
        new_image_name = "neg%d.jpg" % (i)
        new_image_path = "%snegs\\%s" % (REFINED_DIR, new_image_name)
        
        cv2.imwrite(new_image_path, gray)
        
        info += "negs\\%s\n" % (new_image_name)
    
    info_path = REFINED_DIR + "neg_info.data"
    write_file(info_path, info)
    
    print("Done refining")

refine_clouds()
refine_waterspout()
refine_neg()
