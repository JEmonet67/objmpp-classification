#!/home/jerome/anaconda3/bin/python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 10:28:08 2019

Fonction pour réaliser la transformée de Hough afin
d'identifier des cercles dans une image.

@author: jerome
"""

import numpy as np
import cv2 as cv

def Hough_transform(resolution, Par2,mindist,nom):
    #img = cv.imread('''/home/jerome/Stage_Classif_Organoid
    #              /Image_Adrien/07012020-UBTD1-video/Edge2_5.tif''',0)
    img = cv.imread('/home/jerome/Stage_Classif_Organoid/Img_GFP.png',0)
    img = cv.medianBlur(img,5)
    cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
    circles = cv.HoughCircles(img,cv.HOUGH_GRADIENT,resolution,mindist,
                               param1=60,param2=Par2,minRadius=40,maxRadius=220)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
    cv.imwrite(f'/home/jerome/Stage_Classif_Organoid/Img_Transform_Hough/Img1_param_propor_minDistFixed/{nom}',cimg)


#name = "Imgtest.png"
#Hough_transform(1.8,70,50,name)