###############################################################################
## Author: Team Supply Bot
## Edition: eYRC 2019-20
## Instructions: Do Not modify the basic skeletal structure of given APIs!!!
###############################################################################


######################
## Essential libraries
######################
import cv2
import numpy as np
import os
import math
import csv
import imutils

########################################################################
## using os to generalise Input-Output
########################################################################

codes_folder_path = os.path.abspath('.')
images_folder_path = os.path.abspath(os.path.join('..', 'Images'))
generated_folder_path = os.path.abspath(os.path.join('..', 'Generated'))

#Threshold for color [Red, white, green]
lower_range = [np.array([0,100,100]), np.array([0, 0, 212]), np.array([25, 52, 72])]
upper_range = [np.array([0,255,255]), np.array([131, 255, 255]), np.array([102, 255, 255])]


############################################
## Build your algorithm in this function
## ip_image: is the array of the input image
## imshow helps you view that you have loaded
## the corresponding image
############################################
def process(ip_image):
    ###########################
    angle = 0.00
    b_1 = []
    c_1 = []
    hsv = cv2.cvtColor(ip_image, cv2.COLOR_BGR2HSV)
    for i in range(3):
      # Extracting particular color blob from image[Red, green, white]  
      temp = cv2.inRange(hsv, lower_range[i], upper_range[i])
      # Merge Extracting blob and original image
      image1 = cv2.bitwise_and(ip_image,ip_image, mask= temp)
      gray_color = cv2.cvtColor(image1, cv2.COLOR_BGR2GRAY)
      # Blurring image so that noise get reduce
      blurred_color = cv2.GaussianBlur(gray_color, (5, 5), 0)
      thresh_color = cv2.threshold(blurred_color, 60, 255, cv2.THRESH_BINARY)[1]
      # Finding contours of the image
      temp_1 = cv2.findContours(thresh_color.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
      temp_1 = imutils.grab_contours(temp_1)
      for a in temp_1:
        # Finding Center of mass  
        M = cv2.moments(a)
        X = M["m10"]/M["m00"]
        Y = M["m01"]/M["m00"]
        b_1.append(int(X))
        c_1.append(int(Y))
    # Angle between threepoints (a,b,c)
    angle = math.degrees(math.atan2(c_1[2]-c_1[1], b_1[2]-b_1[1]) - math.atan2(c_1[0]-c_1[1], b_1[0]-b_1[1]))
    # if Angle comes out to be negative
    angle = angle + 360 if angle < 0 else angle
    angle = int(360-angle if angle>180 else angle)
    ###########################
    cv2.imshow("window", ip_image)
    cv2.waitKey(0);
    return angle




    
####################################################################
## The main program which provides read in input of one image at a
## time to process function in which you will code your generalized
## output computing code
## Do not modify this code!!!
####################################################################
def main():
    ################################################################
    ## variable declarations
    ################################################################
    i = 1
    line = []
    ## Reading 1 image at a time from the Images folder
    for image_name in os.listdir(images_folder_path):
        ## verifying name of image
        print(image_name)
        ## reading in image 
        ip_image = cv2.imread(images_folder_path+"/"+image_name)
        ## verifying image has content
        print(ip_image.shape)
        ## passing read in image to process function
        A = process(ip_image)
        ## saving the output in  a list variable
        line.append([str(i), image_name , str(A)])
        ## incrementing counter variable
        i+=1
    ## verifying all data
    print(line)
    ## writing to angles.csv in Generated folder without spaces
    with open(generated_folder_path+"/"+'angles.csv', 'w', newline='') as writeFile:
        writer = csv.writer(writeFile)
        writer.writerows(line)
    ## closing csv file    
    writeFile.close()



    

############################################################################################
## main function
############################################################################################
if __name__ == '__main__':
    main()
