# Takes a screen shot of area of screen (defined by region_of_interest).
# Appends pixeldata from screen shot, 
# as well is if the car was going left [1,0,0], forward [0,1,0] or right [0,0,1].

import time
import numpy as np
import math
import glob
import cv2
import random
import time
from SpeedReaderSVM import Train_Svm, Get_Speed, Cap_Speed
from sklearn import svm
from GrabScreen import grab_screen
from KeyCheck import keycheck
from UseKeys import PressKey,ReleaseKey, W, S

ROI = (460,300,1460,760) # Dimensions of the screen you want to capture.
DATA_DIR = "" # Put the directory where your data is kept, "ex C:\\Users\\Alexander\\Desktop\\data\\"

list_f = []
list_lf = []
list_rf = []

amount_of_files = len(glob.glob( DATA_DIR + "*.npy"))
SAVE_DIR = DATA_DIR + str(amount_of_files)

def split_list(a_list, size_of_packages): # If you gather a lot of data, might be wise to split into several packages.
    list_of_lists = []
    i = 0
    while True:
        if len(a_list[i:]) > size_of_packages:
            list_of_lists.append(a_list[i:(i+size_of_packages)])
            i += size_of_packages
        else:
            list_of_lists.append(a_list[i:])
            break

    return list_of_lists

def equalize_data(lf,f,rf): # Makes sure data is balanced, ie you have equal amounts of every data according to label.
    training_data = []
    smallest_value = min([len(lf), len(f), len(rf)]) 
    print("Amount of data: " + str(smallest_value))
    while True:
        
        if not(len(lf) <= smallest_value):
            lf.pop(random.randrange(len(lf)))
            continue
        
        if not(len(f) <= smallest_value):
            f.pop(random.randrange(len(f)))
            continue

        if not(len(rf) <= smallest_value):
            rf.pop(random.randrange(len(rf)))
            continue
            
        break

    for i in lf:
        training_data.append(i)
    for i in f:
        training_data.append(i)
    for i in rf:
        training_data.append(i)
    
    random.shuffle(training_data)
    return training_data

# Train support vector machine (SVM), responsible for reading speed indicator.
clf = Train_Svm()

# Just a time to get user ready.
for i in range(4): 
    print(i+1)
    time.sleep(1)

while True:

    speed = Get_Speed(clf) # Get current speed.
    Cap_Speed(speed) # Make sure we aren't going too fast.

    img = grab_screen(region = ROI)
    img_invert = img.copy()
        
    img = np.array(img)        
    img = cv2.resize(img, (120,60))
    pic_array = img.reshape(60,120,3)

    img_invert = cv2.flip(img_invert,1)
    img_invert = np.array(img_invert)        
    img_invert = cv2.resize(img_invert, (120,60))
    pic_array_invert = img_invert.reshape(60,120,3)

        

    x = keycheck()
    if 'G' in x: # Pressing G on your keyboard shows you the amount of data gathered and the saves,
                 # it to directory provided by SAVE_DIR variable and updates SAVE_DIR.
        print("Saving..")
        print("\n\n\n\n\n\n\n")
        print("Left/Forward: " + str(len(list_lf)))
        print("Forward: " + str(len(list_f)))
        print("Right/Forward: " + str(len(list_rf)))
        time.sleep(1)

        print("Equalizing data...") # Make data balanced.
        training_data = equalize_data(list_lf,list_f,list_rf)

        print("Splitting packages") # Split list of data if it's too large.
        packets = split_list(training_data,10000)

        print("Saving packages") # Saving. 
        for i in packets:
            np.save(SAVE_DIR, i)

        list_f = [] # Clears data lists so we don't save the same data over and over.
        list_lf = []
        list_rf = []

        amount_of_files += 1
        SAVE_DIR = DATA_DIR + str(amount_of_files) # Updates saving dir.
        print("Packages saved!")

    elif ('A' in x) and ('W' in x): # If we're going to the left.
        list_lf.append([pic_array, np.array([1,0,0],dtype='Float32')])
        list_rf.append([pic_array_invert, np.array([0,0,1],dtype='Float32')])

    elif ('D' in x) and ('W' in x): # If we're going to the right.
        list_rf.append([pic_array, np.array([0,0,1],dtype='Float32')])
        list_lf.append([pic_array_invert, np.array([1,0,0],dtype='Float32')])

    elif 'W' in x: # If we're going forward.
        list_f.append([pic_array, np.array([0,1,0],dtype='Float32')])

    elif 'K' in x: # Or just use ctrl + c on windows.
        print("Shutting down")
        break
    else:
        continue # If none of the buttons we're interested in is pressed.