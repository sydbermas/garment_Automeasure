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


def pom():

    # cap = cv.VideoCapture(2, cv.CAP_DSHOW)
    # ret, frame1 = cap.read()
    # (grabbed, frame1) = cap.read()
    # showimg = frame1
    # # cv.imshow('img1', showimg)  # display the captured image
    # cv.waitKey(1)
    # time.sleep(0.3) # Wait 300 miliseconds
    # image = 'camtest\\imagecam.jpeg'
    # cv.imwrite(image, frame1)
    # cap.release()
            

    imageToBeInspected = 'calresult\\imageCap.jpg'    #acting as camera
    pomID = '7M71906MFRONT LENGTH - FROM HPS'
    # imageToBeInspected = 'original.jpeg'
    # poms = [['cropped3.jpeg','cropped4.jpeg']]  
                                                                                                            #Below-ARMHole
    # try :
    #     poms = [glob.glob('poms\\Below-Armhole\\*.jpg')]
    #     # pomOffset =[[157,393,213,350]]
    #     pomOffset =[[20,50,20,50]]
    #     # pomOffset =[[0,0,0,0]]
    #     pomIndex = 0
    #     pixelToInch = 14.50 #camera height - 39 inches to 40
    #     # pixelToInch = 39.50
    #     resultA = []

    #     for pom in poms:

    #         img = cv.imread(imageToBeInspected,0)
    #         img2 = img.copy()
            
    #         templAB = cv.imread(pom[0],0) # pom start
    #         templBA = cv.imread(pom[1],0)
    #         w, h = templAB.shape[::-1]
    #         w2, h2 = templBA.shape[::-1]
    #         # All the 6 methods for comparison in a list
    #         methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
    #                 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    #         meth = methods[1] # Mehtod setting
    #         img = img2.copy()
    #         methodAB = eval(meth)
    #         # Apply template Matching
    #         res = cv.matchTemplate(img,templAB,methodAB)
    #         res2 = cv.matchTemplate(img,templBA,methodAB)
          
    #         min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    #         min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(res2)
            
            
    #         # print(min_val, max_val, min_loc, max_loc)
    #         # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    #         if methodAB in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
    #             top_left = min_loc
    #             top_left2 = min_loc2
               
    #         else:
    #             top_left = max_loc
    #             top_left2 = max_loc2
              
                
    #         pomA = (top_left[0] + pomOffset[pomIndex][0], top_left[1] + pomOffset[pomIndex][1])
    #         pomA2 = (top_left2[0] + pomOffset[pomIndex][2], top_left2[1] + pomOffset[pomIndex][3])
            
    #         resultA.append((pomA2[0]-pomA[0])/pixelToInch)
    #         print("pom-BelowArmhole:",round(resultA[pomIndex],2),"inches") # pom end
           
    # except:
    #     print("Error in POM Below Armhole!")  
  
                                                                                                               #Sweep-Straight
    # try :
    #     poms = [glob.glob('poms\\Sweep-Straight\\*.jpg')]
    #     # pomOffset =[[157,393,213,350]]
    #     pomOffset =[[20,45,35,60]]
    #     # pomOffset =[[0,0,0,0]]
    #     pomIndex = 0
    #     pixelToInch = 16 #camera height - 39 inches to 40
    #     # pixelToInch = 39.50
    #     resultB = []

    #     for pom in poms:

    #         img = cv.imread(imageToBeInspected,0)
    #         img2 = img.copy()
            
    #         templAB = cv.imread(pom[0],0) # pom start
    #         templBA = cv.imread(pom[1],0)
    #         w, h = templAB.shape[::-1]
    #         w2, h2 = templBA.shape[::-1]
    #         # All the 6 methods for comparison in a list
    #         methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
    #                 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    #         meth = methods[1] # Mehtod setting
    #         img = img2.copy()
    #         methodAB = eval(meth)
    #         # Apply template Matching
    #         res = cv.matchTemplate(img,templAB,methodAB)
    #         res2 = cv.matchTemplate(img,templBA,methodAB)
    #         min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    #         min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(res2)
    #         # print(min_val, max_val, min_loc, max_loc)
    #         # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    #         if methodAB in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
    #             top_left = min_loc
    #             top_left2 = min_loc2
               
    #         else:
    #             top_left = max_loc
    #             top_left2 = max_loc2
               
                
    #         pomB = (top_left[0] + pomOffset[pomIndex][0], top_left[1] + pomOffset[pomIndex][1])
    #         pomB2 = (top_left2[0] + pomOffset[pomIndex][2], top_left2[1] + pomOffset[pomIndex][3])
          
    #         resultB.append((pomB2[0]-pomB[0])/pixelToInch)
         
    #         print("pom-SweepStraight:",(round(resultB[pomIndex],3)),"inches") # pom end
         
  
    # except:
    #     print("Error in POM SweepStraight!")  

    #                                                                                                        #Neck width s2s
                                                                                                           
    # try:

    #     poms = [glob.glob('poms\\Neck-Width-S2S\\*.jpg')]
    #     # pomOffset =[[157,393,213,350]]
    #     pomOffset =[[5,18,15,15]]
    #     # pomOffset =[[0,0,0,0]]
    #     pomIndex = 0
    #     pixelToInch = 16 #camera height - 39 inches to 40
    #     # pixelToInch = 39.50
    #     resultC = []

    #     for pom in poms:

    #         img = cv.imread(imageToBeInspected,0)
    #         img2 = img.copy()
            
    #         templAB = cv.imread(pom[0],0) # pom start
    #         templBA = cv.imread(pom[1],0)
    #         w, h = templAB.shape[::-1]
    #         w2, h2 = templBA.shape[::-1]
    #         # All the 6 methods for comparison in a list
    #         methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
    #                 'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    #         meth = methods[1] # Mehtod setting
    #         img = img2.copy()
    #         methodAB = eval(meth)
    #         # Apply template Matching
    #         res = cv.matchTemplate(img,templAB,methodAB)
    #         res2 = cv.matchTemplate(img,templBA,methodAB)
    #         min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    #         min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(res2)
    #         # print(min_val, max_val, min_loc, max_loc)
    #         # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    #         if methodAB in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
    #             top_left = min_loc
    #             top_left2 = min_loc2
               
    #         else:
    #             top_left = max_loc
    #             top_left2 = max_loc2
              
                
    #         pomC = (top_left[0] + pomOffset[pomIndex][0], top_left[1] + pomOffset[pomIndex][1])
    #         pomC2 = (top_left2[0] + pomOffset[pomIndex][2], top_left2[1] + pomOffset[pomIndex][3])
          
    #         resultC.append((pomC2[0]-pomC[0])/pixelToInch)
           
    #        # Return True
           
    #         print("Neck-Width(S2S):",round(resultC[pomIndex],3),"inches") # pom end
  
    # except:
    #     print("Error in POM Neck width s2s!")  
    
    #                                                                                                           #FRONT LENGTH - FROM HPS
                                                                                                           
    try:

        cell = SamplePOMSheet.find(pomID)
        pomID1 = (cell.row, cell.col)
        # pomOffset =[[157,393,213,350]]
        pomOffset = [[SamplePOMSheet.cell(pomID1[0],11).value]]
        poms = [glob.glob('poms\\FrontNeck-FromHPS\\*.jpg')]
        # pomOffset =[[0,0,0,0]]
        pomIndex = 0
        pixelToInch = 16 #camera height - 39 inches to 40
        # pixelToInch = 39.50
        resultD = []

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
        
    # cv.line(img,pomA, pomA2, 255, 1)    #pom below armhole
    # cv.putText(img, "->A: "+ str(round(resultA[pomIndex],3)) , (pomA), cv.FONT_HERSHEY_SIMPLEX, 0.4, (36,255,12), 1)
    # cv.line(img,pomB, pomB2, 255, 2)    #pom sweep straight
    # cv.putText(img, "->B: "+ str(round(resultB[pomIndex],3)) , (pomB), cv.FONT_HERSHEY_SIMPLEX, 0.4, (36,255,12), 2)
    # cv.line(img,pomC, pomC2, 255, 2)    #neck width seam to seam
    # cv.putText(img, "->C: "+ str(round(resultC[pomIndex],3)) , (pomC), cv.FONT_HERSHEY_SIMPLEX, 0.4, (36,255,12), 2)
    cv.line(img,pomD, pomD2, 255, 2)    #Front length- from HPS
    cv.putText(img, "->D: "+ str(round(resultD[pomIndex],2)) , (np.add(pomD,[0,250])), cv.FONT_HERSHEY_SIMPLEX, 0.4, (36,255,12), 2, -1, )
                                                           # Result box
    # root = Tk()
    # root.withdraw()
    # tkinter.messagebox.showinfo(title="Result", message=(
    #     "BelowArmhole:",round(resultA[pomIndex],3),"inches",
    # "\n SweepStraight:",round(resultB[pomIndex],3),"inches",
    # "\n Neck-Width(S2S):",round(resultC[pomIndex],3),"inches",
    # "\n FrontNeck-FromHPS:",round(resultD[pomIndex],3),"inches"))
    # root.destroy()
    
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