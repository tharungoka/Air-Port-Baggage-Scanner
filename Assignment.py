#!/usr/bin/env python

# Importing Required libraries
import cv2
import numpy as np
from PIL import Image
import os

# Paths of 2 sets of input images and output saving path
back_path = 'background_images'
threat_path = 'threat_images'
output_path = 'output'

# List of image file in each of given sets
back_imgs = os.listdir(back_path)
threat_imgs = os.listdir(threat_path)


# For loop over no of images given
for i in range(len(back_imgs)):
    
    # Reading images using OpenCV -- BY default OpenCV readn in BGR
    back_img = cv2.imread(os.path.join(back_path,back_imgs[i]))
    threat_img = cv2.imread(os.path.join(threat_path,threat_imgs[i]))

    # Converting BGR space to RGB space
    back_img = cv2.cvtColor(back_img,cv2.COLOR_BGR2RGB)
    threat_img = cv2.cvtColor(threat_img,cv2.COLOR_BGR2RGB)
    
    # Shape of the background image
    shape = back_img.shape
    
    # White Backgrounded image (shape is taken from background image)
    white = np.full(shape,
                    255, dtype=np.uint8)
    
    # getting the pixels of the threat object only
    threat_object = np.all(threat_img != (255,255,255),2)
    threat_object = threat_object.astype(np.uint8)

    # Finding contours of the threat-object (threat object)
    cnts,_ = cv2.findContours(threat_object,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    # Filling threat object portion with only one color to get the single contour
    result = cv2.fillPoly(threat_object,
                         cnts,
                         (255,255,255))

    # After filling threat object there is some border with other color so drawing the border with same color
    result = cv2.polylines(result,
                         cnts,
                         True,
                         (255,255,255),
                         30)

    # Finding contours of a threat object (only one contour)                     
    cnts,_ = cv2.findContours(result,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    # Getting a bounding box of the threat object
    x,y,w,h = cv2.boundingRect(cnts[0])

    # Cropping threat object 
    cropped_contour= threat_img[y:y+h, x:x+w]
    
    # pasting  cropped image on the white backgrounded image of size same as background image
    first_image = Image.fromarray(white)  # reading image from an array using PIL.Image
    second_image = Image.fromarray(cropped_contour)
    first_image.paste(second_image, (shape[0] // 4,shape[1] //4)) # pasting threat object on the white backrounded object starting from x=shape[0] // 4, y=shape[1] //4
    first_image = np.array(first_image)
    
    # Rotating threat object 45 degrees
    first_img = first_image
    (h,w) = first_img.shape[:2]
    (cX,cY) = (w // 2, h // 2)
    rotation_matrix = cv2.getRotationMatrix2D((cX,cY), 45, 1.0)
    first_img_rotated = cv2.warpAffine(first_img,rotation_matrix,(w,h))

    # After rotation we will get some black portions in rotated image
    # Getting contours of black portions
    black = np.all(first_img_rotated==(0,0,0),2)
    black = black.astype(np.uint8)
    cnts,_ = cv2.findContours(black,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)

    # Filling black portion of rotated image with white color
    first_img_rotated = cv2.fillPoly(first_img_rotated,
                                 cnts,
                                 (255,255,255))
    first_img_rotated = cv2.polylines(first_img_rotated,
                                 cnts,
                                 True,
                                 (255,255,255),
                                 3)

    # Weight for adding -- alpha*first_img + (1-alpha)*back_img + gamma
    alpha = 0.7
    cv2.addWeighted(first_img_rotated,alpha,back_img,1-alpha,0,back_img)

    # Saving output image in output folder
    cv2.imwrite(os.path.join(output_path,str('output'+str(i)+'.jpg')),cv2.cvtColor(back_img,cv2.COLOR_BGR2RGB))

    #Showing image using Opencv
    cv2.imshow('Output',cv2.cvtColor(back_img,cv2.COLOR_BGR2RGB))
    cv2.waitKey(0)



