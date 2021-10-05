import math
from os import replace
import tkinter
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import glob
import imutils
import time
from fractions import Fraction
from tkinter import *
from numpy.core.fromnumeric import amax, shape, var
from numpy.lib.function_base import median
from math import dist
from scipy.spatial import distance
from collections import namedtuple
from itertools import product
import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ["https://spreadsheets.google.com/feeds",
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"]

#CREDENTIALS FROM GOOGLE SERVICE ACCOUNT
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1Pfn_Dx_hEWGChU74iamO3BM4giSL7MpbuepGVo6_Bpk")  
SamplePOMSheet = sheet.worksheet("RAWDATA")
SamplePOMSheet = sheet.worksheet("subImg1")
SamplePOMSheet = sheet.worksheet("subImg2")
stylenum = ""   # will use for entering stylenum
stylesize = "" # also for style size

def pom():

    imageToBeInspected = 'calresult\\imageCap.jpg'    #acting as camera
    pomID = '7M71906MFRONTLENGTH-FROMHPS'
   
    try:

        cell = SamplePOMSheet.find(pomID)
        pomID1 = (cell.row)
        # pomOffset =[[20,10,300,50]]
        offsetX = int(SamplePOMSheet.cell(pomID1,11).value)
        offsetY = int(SamplePOMSheet.cell(pomID1,12).value)
        offsetX2 = int(SamplePOMSheet.cell(pomID1,13).value)
        offsetY2 = int(SamplePOMSheet.cell(pomID1,14).value)
        pomOffset = [[offsetX,offsetY,offsetX2,offsetY2]]
        print(pomOffset)
        
        pomIndex = 0
        pixelToInch = 16 #camera height - 39 inches to 40
        
        resultD = []

        # for pom in poms:

        img = cv.imread(imageToBeInspected,0)
        
        img2 = img.copy()
        
        templAB = (SamplePOMSheet.cell(pomID1,9).value) 
        templBA = (SamplePOMSheet.cell(pomID1,10).value)
        print(templAB)
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
        
        # print(min_loc, max_loc, min_loc2, max_loc2)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if methodAB in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
            top_left = min_loc
            top_left2 = min_loc2
            
        else:
            top_left = max_loc
            top_left2 = max_loc2

        pomD = (top_left[0] + pomOffset[pomIndex][0], top_left[1] + pomOffset[pomIndex][1])
        
        pomD2 = (top_left2[0] + pomOffset[pomIndex][2], top_left2[1] + pomOffset[pomIndex][3])
        
        resultD.append((pomD2[1]+pomD[1])/pixelToInch)

        # Return True
        
        print("FrontLength-FromHPS:",round(resultD[pomIndex],2),"inches") # pom end
  
    except NameError as e:
        print(e)
        

    cv.rectangle(img,pomD, pomD2, 255, 2)    #Front length- from HPS
    cv.putText(img, "->D: "+ str(round(resultD[pomIndex],2)) , (np.add(pomD,[0,250])), cv.FONT_HERSHEY_SIMPLEX, 0.4, (36,255,12), 2, -1, )
                                                           # Result box
    
    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
                                                                # Result end
    
    plt.suptitle(meth)
    mng = plt.get_current_fig_manager()
    mng.window.state("zoomed")
    plt.show()
    pomIndex +=1    #pomindex a to b


pom() # offset test