import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import glob
import imutils
import time

cap = cv.VideoCapture(2, cv.CAP_DSHOW)

ret, frame = cap.read()
(grabbed, frame) = cap.read()
showimg = frame
cv.imshow('img1', showimg)  # display the captured image
cv.waitKey(1)
time.sleep(0.3) # Wait 300 miliseconds
image = 'camtest\\imagecam.jpeg'
cv.imwrite(image, frame)
cap.release()
        

imageToBeInspected = 'camtest\\imagecam.jpeg'    #acting as camera
# imageToBeInspected = 'original.jpeg'
# poms = [['cropped3.jpeg','cropped4.jpeg']]  
poms = [glob.glob('styleNum\\*.jpg')]
# pomOffset =[[157,393,213,350]]
pomOffset =[[30,100,35,90]]
pomIndex = 0
pixelToInch = 16
# pixelToInch = 39.50
result = []

for pom in poms:

    img = cv.imread(imageToBeInspected,0)
    img2 = img.copy()
    template = cv.imread(pom[0],0)
    template2 = cv.imread(pom[1],0)
    w, h = template.shape[::-1]
    w2, h2 = template2.shape[::-1]
    # All the 6 methods for comparison in a list
    methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
            'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
    meth = methods[1] # Mehtod setting
    img = img2.copy()
    method = eval(meth)
    # Apply template Matching
    res = cv.matchTemplate(img,template,method)
    res2 = cv.matchTemplate(img,template2,method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
    min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(res2)
    # print(min_val, max_val, min_loc, max_loc)
    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
        top_left2 = min_loc2
    else:
        top_left = max_loc
        top_left2 = max_loc2
    pomA = (top_left[0] + pomOffset[pomIndex][0], top_left[1] + pomOffset[pomIndex][1])
    pomB = (top_left2[0] + pomOffset[pomIndex][2], top_left2[1] + pomOffset[pomIndex][3])
    print(pomA,pomB)
    result.append((pomB[0]-pomA[0])/pixelToInch)
    print(round(result[pomIndex],3))

    cv.rectangle(img,pomA, pomB, 255, 3)
    # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(121),plt.imshow(img,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
    plt.show()
    pomIndex +=1

