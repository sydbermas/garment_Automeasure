import cv2 as cv
import numpy as np
import glob
from matplotlib import pyplot as plt

#empty list to store template images
template_data=[]
#make a list of all template images from a directory
files1= glob.glob('templates\\*.png')

for myfile in files1:
    image = cv.imread(myfile,0)
    template_data.append(image)

test_image=cv.imread('original.png')    # acting camera
test_image= cv.cvtColor(test_image, cv.COLOR_BGR2GRAY)
methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
#loop for matching
for tmp in template_data:
    (tH, tW) = tmp.shape[:2]
    cv.imshow("Template", tmp)
    cv.waitKey(1000)
    cv.destroyAllWindows()
    for meth in methods:
        method = eval(meth)
    
    result = cv.matchTemplate(test_image, tmp, method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
        top_left = min_loc
    else:
        top_left = max_loc

    bottom_right = (top_left[0] + tW, top_left[1] + tH)
    cv.rectangle(test_image,top_left, bottom_right,255, 2)
    plt.subplot(121),plt.imshow(result,cmap = 'gray')
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(test_image,cmap = 'gray')
    plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    plt.suptitle(meth)
plt.show()