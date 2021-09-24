import math
import tkinter
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import glob
import imutils
import time
from fractions import Fraction
from tkinter import *
from numpy.core.fromnumeric import amax, shape
from numpy.lib.function_base import median
from math import dist
from scipy.spatial import distance
from collections import namedtuple
from itertools import product


imageToBeInspected = 'calresult\\imageCap.jpg'    #acting as camera
    # imageToBeInspected = 'original.jpeg'
    # poms = [['cropped3.jpeg','cropped4.jpeg']]  
                                                                                                            #Below-ARMHole
try :
    poms = [glob.glob('poms\\Below-Armhole\\*.jpg')]
    # pomOffset =[[157,393,213,350]]
    pomOffset =[[0,50,50,50]]
    # pomOffset =[[0,0,0,0]]
    pomIndex = 0
    pixelToInch = 16 #camera height - 39 inches to 40
    # pixelToInch = 39.50
    resultA = []

    for pom in poms:

        img = cv.imread(imageToBeInspected,0)
        img2 = img.copy()
        
        templAB = cv.imread(pom[0],0) # pom start
        templBA = cv.imread(pom[1],0)
        w, h = templAB.shape[::-1]
        w2, h2 = templBA.shape[::-1]
        # All the 6 methods for comparison in a list
        methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
        meth = methods[1] # Mehtod setting
        img = img2.copy()
        methodAB = eval(meth)
        # Apply template Matching
        res = cv.matchTemplate(img,templAB,methodAB)
        res2 = cv.matchTemplate(img,templBA,methodAB)
        
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
        min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(res2)
        
        
        # print(min_val, max_val, min_loc, max_loc)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if methodAB in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
            top_left2 = min_loc2
            
        else:
            top_left = max_loc
            top_left2 = max_loc2
            
            
        pomA = (top_left[0] + pomOffset[pomIndex][0], top_left[1] + pomOffset[pomIndex][1])
        pomA2 = (top_left2[0] + pomOffset[pomIndex][2], top_left2[1] + pomOffset[pomIndex][3])

        resultA.append((pomA2[0]-pomA[0])/pixelToInch)
        print("pom-BelowArmhole:",round(resultA[pomIndex],3),"inches") # pom end
        
except:
    print("Error in POM Below Armhole!")    