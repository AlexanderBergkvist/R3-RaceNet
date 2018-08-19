# R3-RaceNet
My Neural Network based AI, for autonomous driving.

Hi, my name is Alexander. I study IT engineering at the University of Uppsala. As of now i have just concluded my freshman year at university, during the year i have been working on an artificial intelligence for autonomous driving. The project was first inspired by a youtube series published by developer Harrison Kinsley (also known as Sentdex). With my project i wanted to demonstrate the capabilities of neural networks and their ability to make succesful decisions in a semi-complex environment. So without further ado here's the project.

Contents:
---
1. Summary of features
2. The files and what they do
3. Result of project
4. How to implement this yourself
5. Final notes

The files and what they do
---
In this repository you'll find the following files, here's just a little handy guide for what they do so it'll be easy for you to set up and make adjustments.

* **GrabScreen.py**, **UseKeys.py** and **KeyCheck.py** are all programs created by other wonderful people. These programs are responsible for handling all the inputs and outputs of the program, mostly using pywin32. From capturing a screenshot of the game to reading what keys are currently being pressed. Credits for all the individual creator are found in the file itself.

* **vjoy.py** is used to control the joystick on the virtual controller, and **vJoyInterface.dll** needs to be in the directory for it to work. You'll also need to download and run an exe file for vjoy https://sourceforge.net/projects/vjoystick/files/latest/download.

* **SpeedReaderSVM.py** is just for reading the speed indicator in the RaceRoom game, i collected pictures of the speed indicator to train the speedreader's support vector machine. This file will probably have to be altered by you, since your screen probably have a different resolution than mine. You will also need to collect the pictures that you're going to train the svm with. If you do not intend to interact with the speed of the vehicle, you might as well forget about all of this.

* **GetData.py** is for gathering the data used in the training of the neural network. It shouldn't be more setup required than changing the **ROI** to fit the window you play your game in, as well as providing the directory where you want to save the data. After that's done it should simply be matter of driving with the A,W,D keys on your keyboard.

* **TrainModel.py** also fairly straightforward, simply provide the directory where your data is stored. And the you should be good to go!

* **Model.py** is where you find the architecture of the model, maybe you can find an even more efficient model that can outperform mine :)

* **Drive.py** when your AI is trained and ready to go, and vjoy is set up here is where you come to drive your car!



