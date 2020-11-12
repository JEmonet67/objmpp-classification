from objmpp_classification.objets.Point import Point
from objmpp_classification.objets.ObjetMpp import ObjetMpp
import numpy as np
from PIL import Image
import cv2 as cv

class ImgObjMpp:
    
    def __init__(self,path_image,centers_x,centers_y,major_axis):
        self.n_object = len(centers_x)
        self.list_object = []
        
        for i in range(0,self.n_object):
            self.list_object += [ObjetMpp(Point(centers_x,centers_y),major_axis)]

        img = np.array(Image.open(path_image))
        img_global_norm = cv.normalize(img, np.zeros(img.shape),0, 255, cv.NORM_MINMAX)
        self.matrix = np.uint8(img_global_norm)
        #self.matrix = np.uint8(cv.normalize(np.array(Image.open(path_image)), np.zeros(np.array(Image.open(path_image)).shape),0, 255, cv.NORM_MINMAX))
