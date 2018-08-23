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

One problem with the original program was the usage of keys on the keyboard for steering. Usually neural networks predict all possibilities in percentages. For example one output of the neural network could be; 10% Left, 35% Forward, 55% Right. However there was no way to make the car turn more on aggresively the higher the turn percentage got. An 75% right turn would be treated exactly the same as an 85% or 95%, this was because keys only have one state: pressed!

In an stackoverflow discussion https://stackoverflow.com/questions/43483121/simulate-xbox-controller-input-with-python, there was some great advice how to implement a simulated joystick. This allowed the program to become a lot more fluent in it's driving. The joystick took a number between -1 (pulling the joy all the way to the left) and 1 (to the right). So this was implement, the program now takes the probability of a right turn (ex. 0.45) and subtracts probablity of left turn (ex. 0.10). 0.45 - 0.10 = +0.35, so pulling the joystick 35% to the right would be the action generated. In the end I decided to cube the decision to minimize low (uncertain) decisions, for example 0.35^3 = 0.043. I'll provide instruction later in the guide to how to get the joystick to work.  


The files and what they do
---
In this repository you'll find the following files, here's just a little handy guide for what they do so it'll be easy for you to set up and make adjustments.

* **GrabScreen.py**, **UseKeys.py** and **KeyCheck.py** are all programs created by other wonderful people. These programs are responsible for handling all the inputs and outputs of the program, mostly using pywin32. From capturing a screenshot of the game to reading what keys are currently being pressed. Credits for all the individual creator are found in the files.

* **vjoy.py** is used to control the joystick on the virtual controller, and **vJoyInterface.dll** needs to be in the directory for it to work. Source for the file and the testfile: https://gist.github.com/Flandan/fdadd7046afee83822fcff003ab47087#file-vjoy-py

Note: You'll also need to download and run an exe file for vjoy https://sourceforge.net/projects/vjoystick/files/latest/download. 

* **SpeedReaderSVM.py** is just for reading the speed indicator in the RaceRoom game, i collected pictures of the speed indicator to train the speedreader's support vector machine. This file will probably have to be altered by you, since your screen probably have a different resolution than mine. You will also need to collect the pictures that you're going to train the svm with. If you do not intend to interact with the speed of the vehicle, you might as well forget about all of this.

* **GetData.py** is for gathering the data used in the training of the neural network. It shouldn't be more setup required than changing the **ROI** (Region of interest) to fit the window you play your game in, as well as providing the directory where you want to save the data. After that's done it should simply be matter of driving with the A,W,D keys on your keyboard.

* **TrainModel.py** also fairly straightforward, simply provide the directory where your data is stored. And then you should be good to go!

* **Model.py** is where you find the architecture of the model, maybe you can find an even more efficient model that can outperform mine :)

* **Drive.py** when your AI is trained and ready to go, and vjoy is set up here is where you come to drive your car!

How to implement this yourself
---

Because I want anybody to be able to easily get started and try out my project, I'll make this section as straight forward as I possibly can. Follow the instructions to the dot and everything should work for you. Note this will only work on windows because of the pywin32 stuff.

**Instructions**
1. The files
* Clone this repository.
* **GetData.py**, **Drive.py** have two variables: **ROI** (measurements of game window) and **DATA_DIR** (Path to directory where you will keep you data). Supply those with your values and you should be set. The file **SpeedReaderSVM.py** also wants a directory where you keep the data for training it to read the speed indicator. But to use that file you'll need to do a lot more modifying to make it work for your measurements. You might want to leave the speedcap deactivated and just go in novice mode in the game.

2. Vjoy and XBOX360CE

*Vjoy lets us simulate that we have a joystick, XBOX360CE turns those imaginary joystick movements into a format indentical to a real XBOX360 controller.*
* Make sure the DLL provided in the repository is in the directory of the program.
* Download and run this https://sourceforge.net/projects/vjoystick/files/latest/download.
* Get the 64 bit version of this http://www.x360ce.com, then put it into your game directory. For RaceRoom, find the steam. folder then ->\Steam\steamapps\common\raceroom racing experience.
* Now Run the exe file just click through any questions that pops up, XBOX360CE should find vjoy at this point. To test it runt the test file I've provided in the directory.
