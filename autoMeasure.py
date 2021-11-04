from os import name, system
import sys
from tkinter.constants import HORIZONTAL, LEFT, RIGHT
from types import FrameType
from matplotlib import pyplot as plt
import numpy as np
import cv2 as cv
import tkinter as tk
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import gspread
from numpy import empty
from numpy.typing import _16Bit
from oauth2client.client import Error
from oauth2client.service_account import ServiceAccountCredentials
import time
import sys, time
import math
import itertools
scope = ["https://spreadsheets.google.com/feeds",
        'https://www.googleapis.com/auth/spreadsheets',
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"]

#CREDENTIALS FROM GOOGLE SERVICE ACCOUNT
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open_by_key("1Pfn_Dx_hEWGChU74iamO3BM4giSL7MpbuepGVo6_Bpk")  
styleDtlSheet = sheet.worksheet("code")
SamplePOMSheet = sheet.worksheet("RAWDATA")

#Set up GUI
window = tk.Tk()  #Makes main window
window.wm_title("Ubase Automeasure")
window.config(background="#404040")

#Graphics window
imageFrame = tk.Frame(window, width=600, height=500)
imageFrame.pack(side=LEFT, expand=False)

#Capture video frames
lmain = tk.Label(imageFrame)
lmain.pack(side=LEFT, expand=False) 
cap = cv.VideoCapture(int(styleDtlSheet.cell(2,7).value),cv.CAP_DSHOW)

#Camera frame
def show_frame():
    _, frame = cap.read()
    # frame = cv.flip(frame, 1)
    cv.rectangle(frame, (80, 0), (560, 479), (0, 255, 0), 1, 0)
    cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(10, show_frame) 

# store style details
stylenum = tk.StringVar()
sizeset = tk.StringVar()
view = tk.StringVar()
views = ('Front', 'Back', 'Other')
selected_view = tk.StringVar()
sizes = ('XS', 'S', 'M','L', 'XL', 'XXL')
selected_sizes = tk.StringVar()

#Lauch detection on style
def proceed_clicked():

    # camera frame on tkinter gui
    global prevImg
    _, frame = cap.read()
    cv2image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    prevImg = Image.fromarray(cv2image)
    ImageTk.PhotoImage(image=prevImg)
    if (len(sys.argv) < 2):
        filepath = "result.jpg"
    else:
        filepath = sys.argv[1]
    #save captured frame as image
    print ("Output file to: " + filepath)
    prevImg.save(filepath)

    """ callback when the button clicked
    """
    # post tkinter gui text boxes into google sheet code tab
    msg = f'You entered stylenum: {stylenum.get()}, stylenum: {sizeset_entry.get()}, and view: {view_entry.get()}. Please wait for the result'
    styleDtlSheet.update('B2', stylenum.get())
    styleDtlSheet.update('B3', sizeset_entry.get())
    styleDtlSheet.update('B4', view_entry.get())
    #message box of gui details
    showinfo(
        title='Information',
        message=msg
    )
    # get pomiDs selected from 1 style
    pomIDs = styleDtlSheet.col_values(5)    
    tps = int(styleDtlSheet.cell(2,4).value)
    imageToBeInspected = '7M71906M.jpg'    #acting as camera
    
    #google sheet output on code as writer and store
    final_output = []
    final_id = []

    #slice list into half
    # pomID_1 = len(pomIDs)
    # midpomID_2 = pomID_1//2
    # template matching from style details and images
    jpoms = []
    ipoms = []
    for i in pomIDs[1:(len(pomIDs)/2)]:
        ipoms.append(i)
        break

    for j in pomIDs[(len(pomIDs)/2)]:
        jpoms.append(j)
        break

    for i,j in itertools.product(ipoms,jpoms):
        
        try: 
            
            cell_i = SamplePOMSheet.find(i)
            cell_j = SamplePOMSheet.find(j)
            #cell2 = styleDtlSheet.find(poms)

            pomID_i = (cell_i.row)
            pomID_j = (cell_j.row)

            pomOffset = [[0,0,0,0]]  
            pomUID_i = SamplePOMSheet.cell(pomID_i,2).value
            styleName_i = SamplePOMSheet.cell(pomID_i,3).value
            output_i = 'subImages\\'+styleName_i+'\subImg1\\'+pomUID_i+'.JPG'
            output_ii = 'subImages\\'+styleName_i+'\subImg2\\'+pomUID_i+'.JPG'
            # for j
            pomUID_j = SamplePOMSheet.cell(pomID_j,2).value
            styleName_j = SamplePOMSheet.cell(pomID_j,3).value
            output_j = 'subImages\\'+styleName_j+'\subImg1\\'+pomUID_j+'.JPG'
            output_jj = 'subImages\\'+styleName_j+'\subImg2\\'+pomUID_j+'.JPG'

            # print(pomOffset)
            pomIndex_i = 0
            pomIndex_j = 0
    
            result_i = []
            result_j = []

            img_i = cv.imread(imageToBeInspected,0)
            img_j = cv.imread(imageToBeInspected,0)
            
            img2_i = img_i.copy()
            img2_j = img_i.copy()
            
            templ_i = cv.imread(output_i,0) 
            templ_ii = cv.imread(output_ii,0)
            templ_j = cv.imread(output_j,0) 
            templ_jj = cv.imread(output_jj,0)
            w, h = templ_i.shape[::-1]
            w2, h2 = templ_ii.shape[::-1]
            wj, hj = templ_j.shape[::-1]
            w2j, h2j = templ_jj.shape[::-1]
            # All the 6 methods for comparison in a list
            methods_i = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                    'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
            methods_j = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                    'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
            meth_i = methods_i[1] # Mehtod setting
            meth_j = methods_j[1] # Mehtod setting
            img_i = img2_i.copy()
            img_j = img2_j.copy()
            method_i = eval(meth_i)
            method_j = eval(meth_j)
            # Apply template Matchingpip i
            res_i = cv.matchTemplate(img_i,templ_i,method_i)
            res2_i = cv.matchTemplate(img_i,templ_ii,method_i)
            res_j = cv.matchTemplate(img_j,templ_j,method_j)
            res2_j = cv.matchTemplate(img_j,templ_jj,method_j)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res_i)
            min_val2, max_val2, min_loc2, max_loc2 = cv.minMaxLoc(res2_i)
            min_valj, max_valj, min_locj, max_locj = cv.minMaxLoc(res_j)
            min_val2j, max_val2j, min_loc2j, max_loc2j = cv.minMaxLoc(res2_j)
            
            # print(min_loc, max_loc, min_loc2, max_loc2)
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method_i in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                top_left_i = min_loc
                top_left_ii = min_loc2

            else:
                top_left_i = max_loc
                top_left_ii = max_loc2
            
            if method_j in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
                top_left_j = min_locj
                top_left_jj = min_loc2j

            else:
                top_left_j = max_locj
                top_left_jj = max_loc2j
   
            #python subImages topleft 
            subImgpom_i = (top_left_i[0] + pomOffset[pomIndex_i][0], top_left_i[1] + pomOffset[pomIndex_i][1])
            subImgpom_j = (top_left_j[0] + pomOffset[pomIndex_j][0], top_left_j[1] + pomOffset[pomIndex_j][1])

            subImgpom_ii = (top_left_ii[0] + pomOffset[pomIndex_i][2], top_left_ii[1] + pomOffset[pomIndex_i][3])
            subImgpom_jj = (top_left_jj[0] + pomOffset[pomIndex_j][2], top_left_jj[1] + pomOffset[pomIndex_j][3])

            #result calculation from distances of 2 subImages according from height of camera
            result_i.append((math.sqrt((top_left_ii[0] - top_left_i[0])**2 + (top_left_ii[1] -top_left_i[1])**2))/14.9)
            result_j.append((math.sqrt((top_left_jj[0] - top_left_j[0])**2 + (top_left_jj[1] -top_left_j[1])**2))/14.9)
            
            print(pomUID_i+":",round(result_i[pomIndex_i],2),"inches") # pom end
            print(pomUID_j+":",round(result_j[pomIndex_j],2),"inches") # pom end
                #SamplePOMSheet.update_cell(pomID1, 18 , (round(resultD[pomIndex],2)))
            #push to finalOutput
            final_id.append(pomUID_i)
            final_output.append(round(result_i[pomIndex_i],2))
            final_id.append(pomUID_j)
            final_output.append(round(result_j[pomIndex_j],2))

            cv.line(img_i,subImgpom_i, subImgpom_ii, 255, 1)
            cv.line(img_j,subImgpom_j, subImgpom_jj, 255, 1)    
            cv.putText(img_i, str(round(result_i[pomIndex_i],2)) , (np.add(subImgpom_ii,[0,0])), cv.FONT_HERSHEY_SIMPLEX, 0.4, 255, 1)
            cv.putText(img_i, str(round(result_j[pomIndex_j],2)) , (np.add(subImgpom_jj,[0,0])), cv.FONT_HERSHEY_SIMPLEX, 0.4, 255, 1)
            cv.imwrite('Output\\'+str(pomUID_i)+'.jpg', img_i)
            cv.imwrite('Output\\'+str(pomUID_j)+'.jpg', img_j)
            
            # pomIndex +=1
        except NameError as e:
            print(e)

    #Clear Batch Update History
    sheet.values_clear("code!L2:L10000")
    sheet.values_clear("code!M2:M10000")            

    #Batch Update IDs
    cell_list = styleDtlSheet.range("L2:L"+ str(len(final_id)+1))
    for xx, val in enumerate(final_id):
        cell_list[xx].value = val
    styleDtlSheet.update_cells(cell_list)


    #Batch Update results
    cell_list = styleDtlSheet.range("M2:M"+ str(len(final_output)+1))
    for xx, val2 in enumerate(final_output):
        cell_list[xx].value = val2
    styleDtlSheet.update_cells(cell_list) 

    #Batch Update
    poms = SamplePOMSheet.get_values("A2:U")
    idss = styleDtlSheet.get_values("L2:M")

    print("start")
    for id in range(len(idss)):
        for ig in range(len(poms)):
            if(idss[id][0] == poms[ig][1]):
                print( poms[ig][17]," ", idss[id][1])
                poms[ig][17] = idss[id][1]
                break
    
    r_output = []

    for ik in range(len(poms)):
        r_output.append(poms[ik][17])

    cell_lstA = SamplePOMSheet.range("R2:R" + str(len(r_output)+1))
    for ih, val3 in enumerate(r_output):
       cell_lstA[ih].value = str(val3).strip("'")
    SamplePOMSheet.update_cells(cell_lstA)

    viewcnt = int(styleDtlSheet.cell(2,4).value)
    if viewcnt == len(final_id) :

        showinfo(
            title='Information',
            message="Detection Done!"
        )
    else:
        # plt.subplot(121),plt.imshow(res,cmap = 'gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
                #pomindex a to b
        # plt.subplot(121),plt.imshow(img,cmap = 'gray')
        # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
        # plt.suptitle(meth)
        # mng = plt.get_current_fig_manager()
        # mng.window.state("zoomed")
        # plt.show()  
        showinfo(
            title='Information',
            message="Not yet complete! Please detect other poms."
        )

def clear_clicked():
    
    """ callback when the button clicked
    """
    msg = f'You clear all data results!'
    # SamplePOMSheet.clear('R2:R', "")
    # sheet.values_clear("RAWDATA!R2:R10000")
    # sheet.values_clear("code!H2:H10000")
    # sheet.values_clear("code!L2:L10000")
    # sheet.values_clear("code!M2:M10000")

    showinfo(
        title='Information',
        message=msg
    )
    stylenum.set("")
    selected_sizes.set("")
    selected_view.set("")
    # text.set("")

# stylenums
stylenum_label = ttk.Label(window, text="Style Number:")
stylenum_label.pack(fill='x', expand=False)

stylenum_entry = ttk.Entry(window, textvariable=stylenum)
stylenum_entry.pack(fill='x', expand=False)
stylenum_entry.focus()

# sizesets
sizeset_label = ttk.Label(window, text="Sizeset:")
sizeset_label.pack(fill='x', expand=False)

sizeset_entry = ttk.Combobox(window, textvariable=selected_sizes)
sizeset_entry['values'] = sizes
sizeset_entry['state'] = 'readonly'  # normal
sizeset_entry.pack(fill='x', expand=False)

# views
view_label = ttk.Label(window, text="View:")
view_label.pack(fill='x', expand=False)

view_entry = ttk.Combobox(window, textvariable=selected_view)
view_entry['values'] = views
view_entry['state'] = 'readonly'  # normal
view_entry.pack(fill='x', expand=False)

# detect button
proceed_button = ttk.Button(window, text="Detect", command=proceed_clicked)
proceed_button.pack(fill='x', expand=False)

# reset button
clear_button = ttk.Button(window, text="Reset", command=clear_clicked)
clear_button.pack(fill='x', expand=False)


show_frame()  #Display 2
window.mainloop()  #Starts GUI