#!/home/jerome/anaconda3/bin/python3

import numpy as np
import imageio as io
import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte
import cv2 as cv

from scipy import ndimage as ndi
from skimage.morphology import disk
from skimage.segmentation import watershed
from skimage.filters import rank


def Make_markers(path_image,path_ells,path_ells_érodées,path_output,it):
    
    #ells = plt.imread(path_ells)
    img = cv.imread(path_image)
    #gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    #ret, thresh = cv.threshold(gray,0,255,cv.THRESH_BINARY_INV+cv.THRESH_OTSU)
    
    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv.morphologyEx(path_ells,cv.MORPH_OPEN,kernel, iterations = 2)

    # sure background area
    sure_bg = cv.dilate(opening,kernel,iterations=it)

    # Finding sure foreground area
    #sure_fg = plt.imread(path_ells_érodées)
    sure_fg = path_ells_érodées
    # dist_transform = cv.distanceTransform(opening,cv.DIST_L2,5)
    # ret, sure_fg = cv.threshold(dist_transform,0.7*dist_transform.max(),255,0)
    
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    sure_bg = np.uint8(sure_bg)
    unknown = cv.subtract(sure_bg,sure_fg)
    
    # Marker labelling
    ret, markers = cv.connectedComponents(sure_fg)

    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1

    # Now, mark the region of unknown with zero
    markers[unknown==1] = 0
    
    # plt.imshow(img,cmap=plt.cm.gray)
    # plt.imshow(markers, cmap=plt.cm.nipy_spectral, alpha=.7)
    # plt.savefig(f"{path_output}/Markers.png")
    # plt.close()
    
    return markers


def Seg_Water_meth1(path_image,path_ells,path_ells_érodées,path_output,it):
    
    #Load img and denoizing
    img = cv.imread(path_image)
    img = cv.GaussianBlur(img, (7,7), 5)

    #Generate markers
    markers = Make_markers(path_image,path_ells,path_ells_érodées,path_output,it)

    
    #Watershed algorithm
    markers = cv.watershed(img,markers)
    img[markers == -1] = [255,0,0]
    
    # io.imwrite(f"{path_output}/Markers_méthode_1.png",img)
    
    # plt.imshow(img)
    # plt.show()
    
    
def Seq_Water_meth2(path_image,path_ells,path_ells_érodées,path_output,it):
    
    image = img_as_ubyte(plt.imread(path_image))
    # denoise image
    denoised = rank.median(image, disk(2))

    # find continuous region (low gradient -
    # where less than 10 for this image) --> markers
    # disk(5) is used here to get a more smooth image
    markers = Make_markers(path_image,path_ells,path_ells_érodées,path_output,it)
    # markers = rank.gradient(denoised, disk(5)) < 10
    # markers = ndi.label(markers)[0]

    # local gradient (disk(2) is used to keep edges thin)
    gradient = rank.gradient(denoised, disk(2))

    # process the watershed
    labels = watershed(gradient, markers)

    # display results
    # fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(8, 8),
    #                         sharex=True, sharey=True)
    # ax = axes.ravel()

    # ax[0].imshow(image, cmap=plt.cm.gray)
    # ax[0].set_title("Original")

    # ax[1].imshow(gradient, cmap=plt.cm.nipy_spectral)
    # ax[1].set_title("Local Gradient")

    # ax[2].imshow(markers, cmap=plt.cm.nipy_spectral)
    # ax[2].set_title("Markers")

    # ax[3].imshow(image, cmap=plt.cm.gray)
    # ax[3].imshow(labels, cmap=plt.cm.nipy_spectral, alpha=.7)
    # ax[3].set_title("Segmented")

    # for a in ax:
    #     a.axis('off')
    
    # fig.tight_layout()
    # plt.savefig(f"{path_output}/All_méthode_2.png")
    # plt.close()
    
    plt.imshow(image, cmap=plt.cm.gray)
    plt.imshow(labels, cmap=plt.cm.nipy_spectral, alpha=.7)
    plt.savefig(f"{path_output}/Watershed_segmentation.png")
    plt.close()
    labels_norm = cv.normalize(labels, np.zeros(labels.shape),0, 255, cv.NORM_MINMAX)
    labels = np.uint8(labels_norm)
    io.imwrite(path_output + "/Watershed_labels.png",labels)
    
    
    return labels


# path_image_t = "/home/jerome/Stage_Classif_Organoid/Image_Organoïdes/07012020-UBTD1-video/GFP-02_w24-DAPI.TIF"
# ells = plt.imread("/home/jerome/Bureau/Test_watersh/Img2_WT_Segm.png")
# ells_érodées = plt.imread("/home/jerome/Bureau/Test_watersh/Img2_WT_Segm_Erod.png")
# path_output_t = "/home/jerome/Bureau/Test_watersh"

#Seg_Water_meth1(path_image_t,path_ells_t,path_ells_érodées_t,path_output_t,10)
#Seq_Water_meth2(path_image_t,ells,ells_érodées,path_output_t,10)