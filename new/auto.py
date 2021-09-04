# from main import pom
import tkinter as tk
import os
import cv2
import sys
from PIL import Image, ImageTk
import numpy as np
from imutils import perspective
import imutils
from scipy.spatial import distance as dist
import glob
from matplotlib import pyplot as plt


fileName = os.environ['ALLUSERSPROFILE'] + "\WebcamCap.txt"
cancel = False


def prompt_ok(event = 0):
    global cancel, button, button1, button2
    cancel = True

    button.place_forget()
   
    # button1 = tk.Button(mainWindow, text="Good Image!", command=saveAndExit)
    button2 = tk.Button(mainWindow, text="Try Again", command=resume)
    # button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    button2.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
    # button1.focus()
    saveAndExit()
    calibrate()
    
def calibrate():

        #empty list to store template images
    template_data=[]
    #make a list of all template images from a directory
    files1= glob.glob('Styles\\*.jpg')

    for myfile in files1:
        image = cv2.imread(myfile,0)
        template_data.append(image)

    test_image=cv2.imread('camtest\\imageCap.jpg')    # acting camera
    test_image= cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
    'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    #loop for matching
    for tmp in template_data:
        (tH, tW) = tmp.shape[:2]
        # cv2.imshow("Template", tmp)
        # cv2.waitKey(1000)
        # cv2.destroyAllWindows()
        for meth in methods:
            method = eval(meth)
        
        result = cv2.matchTemplate(test_image, tmp, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)


        if result == []:

            tk.messagebox.showinfo(title="Not calibrated", message="Doesn't match on the table")
            mainWindow.quit()

        else:

            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
                
            else:
                top_left = max_loc
                

            bottom_right = (top_left[0] + tW, top_left[1] + tH)
            print (bottom_right)
            cv2.rectangle(test_image,top_left, bottom_right,255, 2)
            plt.subplot(121),plt.imshow(result,cmap = 'gray')
            plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
            plt.subplot(122),plt.imshow(test_image,cmap = 'gray')
            plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
            plt.suptitle(meth)
    plt.show()

        # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
        #        
                 
        # else:
        #         top_left = min_loc
              
       


def saveAndExit(event = 0):
    global prevImg

    if (len(sys.argv) < 2):
        filepath = "caldirectory\\check.jpg"
    else:
        filepath = sys.argv[1]

    print ("Output file to: " + filepath)
    prevImg.save(filepath)
    # mainWindow.quit()


def resume(event = 0):
    global button1, button2, button, lmain, cancel

    cancel = False

    # button1.place_forget()
    button2.place_forget()

    mainWindow.bind('<Return>', prompt_ok)
    button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
    lmain.after(10, show_frame)

def changeCam(event=0, nextCam=-1):
    global camIndex, cap, fileName

    if nextCam == -1:
        camIndex += 1
    else:
        camIndex = nextCam
    del(cap)
    cap = cv2.VideoCapture(camIndex,cv2.CAP_DSHOW)

    #try to get a frame, if it returns nothing
    success, frame = cap.read()
    if not success:
        camIndex = 2
        del(cap)
        cap = cv2.VideoCapture(camIndex,cv2.CAP_DSHOW)

    f = open(fileName, 'w')
    f.write(str(camIndex))
    f.close()

try:
    f = open(fileName, 'r')
    camIndex = int(f.readline())
except:
    camIndex = 0

cap = cv2.VideoCapture(camIndex,cv2.CAP_DSHOW)  

capWidth = cap.get(3)
capHeight = cap.get(4)
success, frame = cap.read()
if not success:
    if camIndex == 0:
        print("Error, No webcam found!")
        sys.exit(1)
    else:
        changeCam(nextCam=0)
        success, frame = cap.read()
        if not success:
            print("Error, No webcam found!")
            sys.exit(1)

def cam_cal():
    # global cancel, button, button1, button2
    # cancel = True

    # button.place_forget()
    # button_calibrate.place_forget()
    # # button1 = tk.Button(mainWindow, text="Good Image!", command=saveAndExit)
    # button2 = tk.Button(mainWindow, text="Try Again", command=resume)
    # # button1.place(anchor=tk.CENTER, relx=0.2, rely=0.9, width=150, height=50)
    # button2.place(anchor=tk.CENTER, relx=0.8, rely=0.9, width=150, height=50)
    # # button1.focus()
    # saveAndExit()
    print("testing")

mainWindow = tk.Tk(screenName="Start")
mainWindow.resizable(width=False, height=False)
mainWindow.bind('<Escape>', lambda e: mainWindow.quit())
lmain = tk.Label(mainWindow, compound=tk.CENTER, anchor=tk.CENTER, relief=tk.RAISED)
button = tk.Button(mainWindow, text="Calibrate", command=prompt_ok)

button_changeCam = tk.Button(mainWindow, text="Switch Camera", command=changeCam)

lmain.pack()
button.place(bordermode=tk.INSIDE, relx=0.5, rely=0.9, anchor=tk.CENTER, width=300, height=50)
button.focus()

button_changeCam.place(bordermode=tk.INSIDE, relx=0.85, rely=0.1, anchor=tk.CENTER, width=150, height=50)

def show_frame():
    global cancel, prevImg, button

    _, frame = cap.read()
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    prevImg = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=prevImg)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    if not cancel:
        lmain.after(10, show_frame)

show_frame()
mainWindow.mainloop()