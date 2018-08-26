# R3-RaceNet
***My Neural Network based AI, for autonomous driving.***

Hi, my name is Alexander. I study IT engineering at the University of Uppsala. As of now i have just concluded my freshman year at university, during the year i have been working on an artificial intelligence for autonomous driving. The project was first inspired by a youtube series published by developer Harrison Kinsley (also known as Sentdex). With my project i wanted to demonstrate the capabilities of neural networks and their ability to make succesful decisions in a semi-complex environment. So without further ado here's the project.

Contents:
---
1. Summary of features
2. The files and what they do
3. Result of project
4. How to implement this yourself
5. Final notes

1 Summary of features
---

As mentioned earlier this project was inspired by Harrison's youtube series Python plays GTA V, in which he made an AI that could drive on the roads in a scooter. However over the course of my R3's development a lot of things have changed, so here's a brief summary of what you can expect from my solution:

**Speed limit** 

Since I wanted to show the car's ability to drive on the road, there could never be an instance where the car was going to fast to even be able to make a successful turn. To achieve this i capped the car's speed at 50 km/h, by making the car press the brake key slightly when it's speed surpassed that limit. However the method didn't always limit the speed entirely which is why a second, more aggresive brake was implemented at 60 km/h. So the speed would essentially vary in the intervall of 50-60 km/h. This limit could probably have been a little higher, but i figured 50 would be enough to prove the point.

![Speed indicator](https://github.com/sscool12/R3-RaceNet/blob/master/speed_indi.png)

*Reading the speedindicator is simply as matter of capturing all three digits and running them through some lightweight image classifier, like in this case where a support vector machine was used.*

**Lighter model**

Running the popular Alexnet on my old computer wasn't really an option, so a lighter model was implemented. This model was suggested by NVIDIA in one of their talks about driving car simulations. The structure was as follows:

``` 
    network = input_data(none,120,60,3) # Input layer 

    network = conv_2d(network, 24, 5, activation='elu',strides = 2)
    network = conv_2d(network, 36, 5, activation='elu',strides = 2)
    network = conv_2d(network, 48, 5, activation='elu',strides = 2)
    network = conv_2d(network, 64, 3, activation='elu')
    network = conv_2d(network, 64, 3, activation='elu')
    
    network = dropout(network, 0.5)
    
    network = fully_connected(network, 100, activation='elu')
    network = fully_connected(network, 50, activation='elu')
    network = fully_connected(network, 10, activation='elu')
    
    network = fully_connected(network, 3, activation='softmax') # Output layer

    # optimizer : adam
    
```
*This model which was much lighter on the fully connected side also allowed for much faster training.*


**Gathering data**

One thing to note about the datagathering proccess is that most tracks would be heavily biased towards turning one way. For example one track would have 75% right turns and 25% left, this is due to the nature of racing tracks. So an added feature was to always invert the turn as well, saving both the original data sample as well as the inverted one. So for example if a right turn was taken, the program would save that screenshot with according label "right". Then it would invert the picture (mirror it horizontaly), and change the label to "left". The logic here is if we were given the exact opposite turn we would of course take the exact same turn, but in the other direction.

**Joystick Driving**

One problem with the original program was the usage of keys on the keyboard for steering. Usually neural networks predict all possibilities in percentages. For example one output of the neural network could be; 10% Left, 35% Forward, 55% Right. However there was no way to make the car turn more on aggresively the higher the turn percentage got. An 75% right turn would be treated exactly the same as an 85% or 95%, this was because keys only have one state: pressed!

In an stackoverflow discussion https://stackoverflow.com/questions/43483121/simulate-xbox-controller-input-with-python, there was some great advice how to implement a simulated joystick. This allowed the program to become a lot more fluent in it's driving. The joystick took a number between -1 (pulling the joy all the way to the left) and 1 (to the right). So this was implement, the program now takes the probability of a right turn (ex. 0.45) and subtracts probablity of left turn (ex. 0.10). 0.45 - 0.10 = +0.35, so pulling the joystick 35% to the right would be the action generated. In the end I decided to cube the decision to minimize low (uncertain) decisions, for example 0.35^3 = 0.043. I'll provide instruction later in the guide to how to get the joystick to work.  


2 The files and what they do
---
In this repository you'll find the following files, here's just a little handy guide for what they do so it'll be easy for you to set up and make adjustments.

* **GrabScreen.py**, **UseKeys.py** and **KeyCheck.py** are all programs created by other wonderful people. These programs are responsible for handling all the inputs and outputs of the program, mostly using pywin32. From capturing a screenshot of the game to reading what keys are currently being pressed. Credits for all the individual creators are found in the files.

* **vjoy.py** is used to control the joystick on the virtual controller, and **vJoyInterface.dll** needs to be in the directory for it to work. **VjoyTest.py** can be used to test that everything is set up correctly. Source for the file and the testfile: https://gist.github.com/Flandan/fdadd7046afee83822fcff003ab47087#file-vjoy-py

* **SpeedReaderSVM.py** is just for reading the speed indicator in the RaceRoom game, i collected pictures of the speed indicator to train the speedreader's support vector machine. This file will probably have to be altered by you, since your screen probably have a different resolution than mine. You will also need to collect the pictures that you're going to train the svm with. 

    If you do not intend to interact with the speed of the vehicle, you might as well forget about all of this. All usage of this file is commented out by default, this is because you need to change a lot of cordinates for all the screencaptures that are used. Also this solution needs the three digit speed indicator as shown in the picture above. If you'd like to use for example a continous speed indicator like the one in real cars, you'd have to come up with a different solution most likely.

* **GetData.py** is for gathering the data used in the training of the neural network. It shouldn't be more setup required than changing the **ROI** (Region of interest) to fit the window you play your game in, as well as providing the directory where you want to save the data. After that's done it should simply be matter of driving with the A,W,D keys on your keyboard.

* **TrainModel.py** also fairly straightforward, simply provide the directory where your data is stored. And then you should be good to go!

* **Model.py** is where you find the architecture of the model, maybe you can find an even more efficient model that can outperform mine :)

* **Drive.py** when your AI is trained and ready to go, and vjoy is set up here is where you come to drive your car!

3 Results of the project
---

*See for yourself ;)*

[R3 drives through known racing track  ](https://www.youtube.com/watch?v=FQm_RhlMMIk&list=PL87x_8UldN28gSHIorqH8CCt7S98PMn7M)

This footage was from one of the tracks that R3 actually had seen before, the data R3 was trained on was gathered from this track and that's why it does really well here.

[R3 drives through UN-known racing track ](https://www.youtube.com/watch?v=8-deaYUIiac&index=2&list=PL87x_8UldN28ilAxlseKcB5XeUSVrhO0m)

Here is where R3 actually exceded my expectations, this course was purchased after training R3 simply because i wanted to see how it would react to new challenges. I was very suprised to see that it actually made very few mistakes, and it seemed to know what it was doing.

4 How to implement this yourself
---

Because I want anybody to be able to easily get started and try out my project, I'll make this section as straight forward as I possibly can. Follow the instructions to the dot and everything should work for you. Note this will only work on windows because of the pywin32 stuff.

**Instructions**
1. Dependencies

*You'll need the following dependencies, all should just be one simple pip install away.*
* Numpy
* TFlearn and Tensorflow
* Sklearn
* Glob
* PyWin32
* OpenCV

``` pip install numpy tensorflow tflearn sklearn pywin32 opencv-python ```

2. The files
* Clone this repository.
* **GetData.py**, **Drive.py** and **TrainModel.py** have two variables: **ROI** (measurements of game window) and **DATA_DIR** (Path to directory where you will keep you data). Supply those with your values and you should be set. 
* The file **SpeedReaderSVM.py** also wants a directory where you keep the data for training it to read the speed indicator. But to use that file you'll need to do a lot more modifying to make it work for your measurements. You might want to leave the speedcap deactivated and just go in novice mode in the game. This will adjust the speed for you.

3. Vjoy and XBox360CE

*Vjoy lets us simulate that we have a joystick, XBox360CE turns those imaginary joystick movements into a format indentical to a real XBox360 controller.*
* Make sure the DLL provided in the repository is in the directory of the program.
* Download and run this https://sourceforge.net/projects/vjoystick/files/latest/download.
* **vjoy.py** can now be used to control the virtual controller. Now we need to set up XBox360CE
* Get the 64 bit version of this http://www.x360ce.com, then put it into your game directory. For RaceRoom, find the steam. folder then ->\Steam\steamapps\common\raceroom racing experience.
* Now run the file just click through any questions that pops up, XBox360CE should find vjoy at this point. To test it run the test file **VjoyTest.py** I've provided in the directory.

5 Final notes
---
Before you leave I'd just like to thank you for taking the time to check out my project. If you much like me are completely new to neural networks and machine learning in general. And possible is struggling a bit to get started, I hope I've given you some sort of inspiration to keep on going. Learning this sort of stuff can really feel like banging your head against the wall. Just sitting there waiting for hours for your model to train, and then for it to end up not working can lead to some serious frustration. 

But trust me, it gets better. I especially hope you who feel like you're just getting started can have some fun with my program, pick it apart and see if you can come up with something cool of your own. Because that's atleast what have worked for me, and don't pull yourself down if nothing works. I have been working on this on the side parallell to my education, and for the last 6 months i have been on the verge of quiting atleast once a week. So cheer up, and best of luck to you!

If you have any questions for me please just send me an email at alexander.bergkvist@hotmail.com, and I'll do my best to help you out :D
If nothing else... Have a good one!
