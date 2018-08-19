import glob
import numpy as np
import cv2
import time
import random
from SpeedReaderSVM import Train_Svm, Get_Speed, Cap_Speed
from GrabScreen import grab_screen
from UseKeys import PressKey,ReleaseKey, W, S
from Model import model
from sklearn import svm
from vjoy import vj, setJoy

# Parameters and general info.
WIDTH = 60
HEIGHT =120
LR = 1e-3
MODEL_NAME = 'SomeNameHere.model' # Whatever you called it when training.
ROI = (460,300,1460,760)

# Create model and load trained weights.
model = model(WIDTH, HEIGHT, LR)
model.load(MODEL_NAME)

def main():
    scale = 16000.0  # Vjoy stuff.
    vj.open()
    while(True):
        
        speed = Get_Speed(clf) # Get current speed.
        Cap_Speed(speed) # Make sure we aren't going too fast.

        screen = grab_screen(region = ROI)  #Screenshot part of window.
        screen = np.array(screen) #Make screenshot into array.
        screen = cv2.resize(screen, (120,60)) #Resize to a 120x60 pic.
        pic_array = screen.reshape(60,120,3)
        
        prediction = model.predict({'input_pic': [pic_array]})[0]

        steer = (prediction[2] - prediction[0]) ** 3 
        setJoy(steer + 0.024, 0, scale) # +0.024 Helps fix joystick offset.
    vj.close()

# Now lets go!
# Train support vector machine (SVM), responsible for reading speed indicator.
clf = Train_Svm()

# Driving begins.
main() 