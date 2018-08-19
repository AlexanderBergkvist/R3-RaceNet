import tflearn
from tflearn.layers.conv import conv_2d, max_pool_2d
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
import numpy as np
import random
from Model import model
import time
import glob
from sklearn import svm

# Parameters and other info.
WIDTH = 60
HEIGHT = 120
LR = 8e-4
EPOCHS = 2
DATA_DIR = "" # Put the directory where your data is kept, ex C:\\Users\\Alexander\\Desktop\\data\\
MODEL_NAME = 'SomeNameHere.model' # Call it whatever you want.
HM_TEST = 1000 # How many of your training samples you want to set aside as testing samples.

print("Loading data") #Load all your data and divide it into train and test data
all_data = glob.glob( DATA_DIR + "*.npy")

data = np.load(all_data.pop(0))

x=1
for i in all_data:
    data = np.vstack((data,np.load(i)))
    print(str(x) + "/" + str(len(all_data)) + " items loaded!")
    x +=1
print("Data loaded!")

random.shuffle(data) # Shuffle data (important when doing machine learning!)
train_data = data[HM_TEST:]
test_data = data[:HM_TEST]

train_x = [i[0] for i in train_data]
train_y = [i[1] for i in train_data]

test_x = [i[0] for i in test_data]
test_y = [i[1] for i in test_data]




model = model(WIDTH, HEIGHT, LR)

model.fit({'input_pic': train_x}, {'targets': train_y}, n_epoch=EPOCHS,
              validation_set=({'input_pic': test_x} ,{'targets': test_y}), 
              snapshot_step=100, show_metric=True, batch_size = 200,
              validation_batch_size=100)

model.save(MODEL_NAME)       