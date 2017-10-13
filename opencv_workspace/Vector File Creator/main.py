import os
import cv2

opencv_workspace = "C:\\Users\\gaged\\OneDrive\\School\\" + \
        "Cloud Coverage Calculator\\opencv_workspace\\"

dirs = [opencv_workspace + "clouds\\cirrus\\",
        opencv_workspace + "clouds\\cumulus\\",
        opencv_workspace + "clouds\\stratus\\",
        opencv_workspace + "clouds\\waterspout\\",
        opencv_workspace + "negs\\"]

outs = ["", "", "", "", ""]
out_index = 0

print("Should the images be cleaned? [y/n]")
clean = input() == 'y'

RESIZE_SIZE = 24

for dir in dirs:
    print("Generating file text")
    
    # used for cleaning
    counter = 0
    
    for filename in os.listdir(dir):
        if (not filename.endswith(".jpg")) and (not filename.endswith(".png")):
            continue
        
        path = dir + filename
        new_filename = "image_" + str(counter) + ".jpg"
        image = cv2.imread(path)
        
        if clean:
            new_path = dir + new_filename
            new_image_file = open(new_path, "w+")
            
            if out_index == 4:
                cv2.imwrite(new_path, image)
            else:
                resized_image = cv2.resize(image, (24, 24), interpolation = cv2.INTER_AREA)
                cv2.imwrite(new_path, resized_image)
            
            new_image_file.close()
        
            os.remove(path)
        
        if out_index == 4:
            outs[out_index] += new_filename + "\n"
        else:
            outs[out_index] += "%s 1 0 0 %d %d\n" % (new_filename, RESIZE_SIZE, RESIZE_SIZE)
        
        counter += 1
    
    outfile_path = dir + "info.data"
    
    print("Opening file", outfile_path)
    outfile = open(outfile_path, "w+")
    
    print("Writing to file")
    outfile.write(outs[out_index])
    
    print("Closing file\n")
    outfile.close()
    
    out_index += 1
