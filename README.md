# R3-RaceNet
My Neural Network based AI, for autonomous driving.

# This ReadMe isn't finished
Hi, my name is Alexander. I study IT engineering at the University of Uppsala. As of now i have just concluded my freshman year at university, during the year i have been working on an artificial intelligence for autonomous driving. The project was first inspired by a youtube series published by developer Harrison Kinsley (also known as Sentdex). With my project i wanted to demonstrate the capabilities of neural networks and their ability to make succesful decisions in a semi-complex environment. So without further ado here's the project.

Contents:
---
1. Summary of features
2. The files and what they do
3. Result of project
4. How to implement this yourself
5. Final notes

Summary of features
---

As mentioned earlier this project was inspired by Harrison's youtube series Python plays GTA V, in which he made an AI that could drive on the roads in a scooter. However over the course of my R3's development a lot of things have changed, so here's a brief summary of what you can expect from my solution:

**Speed limit** 

Since I wanted to show the car's ability to drive on the road, there could never be an instance where the car was going to fast to even be able to make a successful turn. To achieve this i capped the car's speed at 50 km/h, by making the car press the brake key slightly when it's speed surpassed that limit. However the method didn't always limit the speed entirely which is why a second, more aggresive brake was implemented at 60 km/h. So the speed would essentially vary in the intervall of 50-60 km/h. This limit could probably have been a little higher, but i figured 50 would be enough to prove the point.

**Gathering data**

One thing to note about the datagathering proccess is that most tracks would be heavily biased towards turning one way. For example one track would have 75% right turns and 25% left, this is due to the nature of racing tracks. So an added feature was to always invert the turn as well, saving both the original data sample as well as the inverted one. So for example if a right turn was taken, the program would save that right turn with according label "right". Then it would invert the picture (mirror it horizontaly), and change the label to "left". The logic here is if we were given the exact oppsite turn we would of course take the exact same turn, but in the other direction.

**Joystick Driving**

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



