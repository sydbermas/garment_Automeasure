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
import gdown
from tkinter import *
from tkinter.ttk import *
import time

scope = ["https://spreadsheets.google.com/feeds",
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"]

#CREDENTIALS FROM GOOGLE SERVICE ACCOUNT
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1Pfn_Dx_hEWGChU74iamO3BM4giSL7MpbuepGVo6_Bpk")  
SamplePOMSheet = sheet.worksheet("RAWDATA")
styleDtlSheet = sheet.worksheet("code")



def pom():
    resultCount = styleDtlSheet.cell(2,6).value
    styleCount = styleDtlSheet.cell(2,3).value
    pomIDs = styleDtlSheet.col_values(5)
    print(pomIDs)
    GB = int(styleCount)
    styles = 0
    speed = 1
    

    imageToBeInspected = 'calresult\\imageCap.jpg'    #acting as camera
    # pomID = '7M71906MFRONTLENGTHFROMHPS'   # change later for stylenum while loop
    
    for poms in pomIDs[1:]:

        try:
            
            cell = SamplePOMSheet.find(poms)
            bar['value']+=(speed/GB)*100
            styles+=speed
            percent.set(str(int((styles/GB)*100))+"%")
            text.set(str(styles)+"/"+str(GB)+" Point of measure processed")
            window.update_idletasks()
            pomID1 = (cell.row)
            # pomOffset =[[20,10,300,50]]
            offsetX = int(SamplePOMSheet.cell(pomID1,14).value)
            offsetY = int(SamplePOMSheet.cell(pomID1,15).value)
            offsetX2 = int(SamplePOMSheet.cell(pomID1,16).value)
            offsetY2 = int(SamplePOMSheet.cell(pomID1,17).value)
            pomOffset = [[offsetX,offsetY,offsetX2,offsetY2]]
            pomUID = SamplePOMSheet.cell(pomID1,2).value
            styleName = SamplePOMSheet.cell(pomID1,3).value
            output1 = 'subImages\\'+styleName+'\subImg1\\'+pomUID+'.JPG'
            output2 = 'subImages\\'+styleName+'\subImg2\\'+pomUID+'.JPG'
            print(pomOffset)
            pomIndex = 0
            pixelToInch = 16 #camera height - 39 inches to 40
            resultD = []

            # for pom in poms:

            img = cv.imread(imageToBeInspected,0)
            
            img2 = img.copy()
            
            templAB = cv.imread(output1,0) 
            templBA = cv.imread(output2,0)
            w, h = templAB.shape[::-1]
            w2, h2 = templBA.shape[::-1]
            # All the 6 methods for comparison in a list
            methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                    'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
            meth = methods[1] # Mehtod setting
            img = img2.copy()
            methodAB = eval(meth)
            # Apply template Matchingpip i
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
                print (top_left)
                print (top_left2)

            subImg1pom = (top_left[0] + pomOffset[pomIndex][0], top_left[1] + pomOffset[pomIndex][1])
            
            subImg2pom = (top_left2[0] + pomOffset[pomIndex][2], top_left2[1] + pomOffset[pomIndex][3])
            
            resultD.append((subImg2pom[1]+subImg1pom[1])/pixelToInch)

            # Return True
            
            print(pomUID+":",round(resultD[pomIndex],2),"inches") # pom end
            SamplePOMSheet.update_cell(pomID1, 18 , (round(resultD[pomIndex],2)))
            
        except NameError as e:
            print(e)
            
        cv.rectangle(img,subImg1pom, subImg2pom, 255, 2)    
        cv.putText(img, str(round(resultD[pomIndex],2)) , (np.add(subImg2pom,[0,250])), cv.FONT_HERSHEY_SIMPLEX, 0.4, (36,255,12), 2, -1, )
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

window = Tk()

percent = StringVar()
text = StringVar()

bar = Progressbar(window,orient=HORIZONTAL,length=300)
bar.pack(pady=10)

percentLabel = Label(window,textvariable=percent).pack()
taskLabel = Label(window,textvariable=text).pack()

# pom() # offset test