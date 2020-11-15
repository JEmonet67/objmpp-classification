from objmpp_classification.objects.Point import Point
from objmpp_classification.objects.Organoid import Organoid
import numpy as np
import pandas as pd
from PIL import Image
import cv2 as cv

class ImgObjMpp:
    
    def __init__(self,path_image, path_region, path_csv):
        df_marks = pd.read_csv(path_csv)
        centers_x = df_marks["Center Col"]
        centers_y = df_marks["Center Row"]
        major_axis = df_marks["Semi Major Axis"]
        
        self.n_object = len(centers_x)
        self.list_object = []
        self.list_distmap = []
        self.list_reg_watersh = []
        self.list_img_local_object = []
        
        for i in range(0,self.n_object):
            self.list_object += [Organoid(Point(centers_x[i],centers_y[i]),major_axis[i])]

        self.matrix_img = np.uint8(cv.normalize(np.array(Image.open(path_image)), np.zeros(np.array(
            Image.open(path_image)).shape),0, 255, cv.NORM_MINMAX))
        self.matrix_regions = cv.imread(path_region,0)
        



