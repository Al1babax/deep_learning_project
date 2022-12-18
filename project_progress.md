# Project Progress

## 1. Introduction
The main idea of the project is to track cars from town called Teuva using 
their CCTV camera and applying R-CNN model to it.

## 2. First approach
`test/diff_map_test.py`
`test/cnn_algo.ipynb`
`test/cnn_algo_test.ipynb`

First I tried to use color channel difference between frames to detect if something was moving.

### 2.1 Problems
Biggest problem here was that even leaves/flag pole were counted as moving objects when I wanted to only track cars.
Solution to this was using algorithm that runs kernel area from left to right with size for example (10, 10) pixels.
Then if within that box there was enough pixels color channel change it was counted as moving vehicle.

### 2.2 Saving results
After I got above algorithm working I could use the kernel area as a bounding box for a car and I saved that as a label for that specific frame.
I saved frames and labels this way to automatically annotate data for training a model. (Later on this was not good enough)

### 2.3 Training a model
Trying to train the first model was disaster. Information that the neural network had to output was the location of all the cars,
and classification that they are cars. Only thing I got done here was detecting a singular car from a frame. This was not the right way to approach.

## 3. Second approach
`R-CNN-test/`

https://roboflow.com/ For annotating data

Next I studied how other projects do this and I learned that they use two scripts. One for detecting bounding boxes and
another for just regular classification neural network aka R-CNN model.
I like to call it regional convolution neural network even though it is not right, but it explains what it does.

### 3.1 Detecting bounding boxes
I started building my own script for detecting bounding boxes using search algorithms from open vision library that is
used for computer vision tasks on python. The search algorithm is region proposal that gives bounding boxes of possible
areas that might include an object. 

After that you use  algorithm called IoU which stand for Intersection over union.
With this you can check if the proposed areas are overlapping with your training labels aka bounding boxes for that specific frame.
Then you save images to folder called cars and non-cars to train binary classification model later on.

### 3.2 Training a model
After you have images of non-cars and cars you can train classification model to detect cars from these proposed regions.

### 3.3 Using the model
After all this is done to actually use the whole thing to detect cars from image. You run every frame of the video through 
search algorithm that will propose areas that are then checked through classification neural network to check how many cars
in this proposes there were.

### 3.4 Problems
Biggest problem with this way of doing R-CNN network was that it is way too slow. Running one frame through this
whole pipeline will take between 20-60 seconds depending on parameters. Mainly because search algorithm is super slow.
Fortunately this is the old way, and this model has been improved several times in the past 20 years.

## 4. Third approach
`count_cars/`
`API/`
`batch_scripts/`

https://roboflow.com/ For annotating data

Rather than focusing making myself good R-CNN algorithm with the new search algorithms I decided to just use premade
model and improve on top of it. I chose model called YoloV5.

### 4.1 Learning YoloV5 and CV2
`screen_recorder/`

Out of curiosity and learning I decided to make a screen recording software that could use the R-CNN model called YoloV5
and detect different objects from the live recording. This YoloV5 has been trained with dataset called COCO.
It is a lot of images of different objects, roughly 90 different objects.

### 4.2 Tackling car counting problem
After I was done with the screen recording software I started making car counting script using YoloV5.

### 4.3 Custom training
I custom trained the YoloV5 using video/pictures I got from live video feed from Teuva using scripts in folder `data_gather`.

### 4.4 Detecting
I drew a vertical line to middle of video that I used as area where I counted the cars if cars bounding box ever passed the line.
This way I could track how many cars passed that line.

### 4.5 RestApi
I used logging to save the results, and built small RestAPI that shows the results of cars passing.

### 4.6 Performance
The results are quite accurate for testing videos with error ~1-5%.

For live feed I had worse accuracy. Error ~20-40% . I think there are at least two reasons for this:
- Brightness of the video
- Detection model accuracy on live feed

All this could improve with more training. But only long term solution is tracking
algorithm. 


### 4.7 Problems
Biggest problem was how to accurately count how many cars pass the road.
Problem was at what point do I count a car on the road as passing car and
how not to count one car twice. I had ok solution for this, but much better can be done.

### 4.8 Improvements
To further optimize the performance of the system by fine-tuning the YoloV5 model and implementing
additional techniques such as object tracking to improve the reliability and accuracy of the car tracking system.

I started working on object tracking but did not have enough time to implement it.