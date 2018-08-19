import numpy as np
import glob
import cv2
import random
from sklearn import svm
from GrabScreen import grab_screen
from UseKeys import PressKey,ReleaseKey, W, S

SVM_DATA_DIR = "" #Directory containing data for training SVM, ex C:\\Users\\Alexander\\Desktop\\svm_data\\.


def Train_Svm():
    # Train support vector machine (SVM), responsible for reading speed indicator.
    print("Training SVM!")
    X = []
    Y = [] 
    all_dirs = glob.glob( SVM_DATA_DIR + "*.png") 
    for i in all_dirs:
        file_name = i.split("\\")[-1]
        if file_name.split(".")[1] == "10":
            Y.append(0)
        else:
            Y.append(int(file_name.split(".")[1]))
        image = cv2.imread(i,0)
        hej = image.flatten()
        X.append(hej)
    
    clf = svm.SVC(C=100,gamma=0.001)
    clf.fit(X, Y)
    # SVM trained, return the trained SVM object.
    print("Training DONE!")
    return clf

def Get_Speed(clf):
    # Use SVM to read speed indicator and return the current speed of vehicle.
    img1 = grab_screen(region=(1361,830,1374,853))
    img2 = grab_screen(region=(1348,830,1361,853))
    img3 = grab_screen(region=(1335,830,1348,853))
    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    img3 = cv2.cvtColor(img3, cv2.COLOR_BGR2GRAY)
    img1 = img1.flatten()
    img2 = img2.flatten()
    img3 = img3.flatten()
    pred1 = clf.predict([img1])
    pred2 = clf.predict([img2])
    pred3 = clf.predict([img3])
    return pred3[0]*100 + pred2[0]*10 + pred1[0]

def Cap_Speed(speed):
    # Use speed to slow down car if it's going too fast.
    if speed > 60:
        PressKey(S)
        ReleaseKey(W)
    
    elif speed > 50:
        PressKey(S)

    else:
        PressKey(W)
        ReleaseKey(S)