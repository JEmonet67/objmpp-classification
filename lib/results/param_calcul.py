from decimal import Decimal
from objmpp_classification.processing.intensity_profiling import frange
import numpy as np
import cv2 as cv

def mean_intensity_level(list_somme,list_count,k):
    i_mean = 0
    list_mean = []
    k_cut = k
    while i_mean < k:
        try:
            list_mean += [round(list_somme[i_mean]/list_count[i_mean],2)]
            i_mean += 1
        except ZeroDivisionError:
            i_mean += 1
            k_cut -= 1
            print("Division 0,", i_mean)
    list_mean.reverse()
    
    return list_mean, k_cut

    
def thresholding(list_mean,k):
    ratio = 1/k
    list_diff = []
    list_seuil = list(frange(Decimal(ratio), Decimal(100+ratio), ratio))

    for i_seuil in range(1,len(list_mean)+1):
        sup_seuil = list_mean[i_seuil:]
        inf_seuil = list_mean[:i_seuil]
        diff_integral = round((sum(sup_seuil)-sum(inf_seuil)),2)
        list_diff += [diff_integral]
    
    min_diff = abs(list_diff[0])
    
    for diff in list_diff[1:]:
        if abs(diff) < min_diff:
            min_diff = diff
    
    Index_min = list_diff.index(min_diff)
    
    return round(list_seuil[Index_min],2), min_diff

def middle_part_obj(list_mean,x):
    borne50 = int(len(x) * 0.5)
    list_mean_0_50 = list_mean[:borne50]
    mean_0_50 = np.mean(list_mean_0_50)
    
    return mean_0_50
    
def make_contour(img):
    img_bin = np.copy(img)
    img_bin[img_bin > 0] = 1
    img_laplacian = cv.Laplacian(img_bin,cv.CV_64F)
    img_laplacian = np.absolute(img_laplacian)
    img_laplacian = np.uint8(img_laplacian)
    img_laplacian[img_laplacian>0] = 1
    #io.imwrite(f"{path_output}/Test_contour/Image_laplacian_{i_obj}.png",img_laplacian)
    
    return np.sum(img_laplacian)
    