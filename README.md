# R-CNN project
School project for the course "Deep learning" at Jyväskylän ammattikorkeakoulu.
I decided to make multi-object detection project. The objective was to make model that could be used
to detect cars from livestream CCTV footage. As a side project I made a screen recording software that
can be used to record footage from your screen and applying object detection on it.

## Technologies used
I mainly used YOLOv5 R-CNN models for this project. It is a multi class multi object detection model, that I used as a baseline
for my project. I also used OpenCV for image processing and PySimpleGUI for the GUI.

## Installation
<details>
<summary>Click to expand!</summary>

### Requirements
- Python 3.9 (Newer versions might work, but I haven't tested them)

**Important**
You have to install CUDA and cuDNN to your computer. I used CUDA 11.8.0 and cuDNN. I cannot guarantee
software working without these. Also, it makes software much faster.


### Installation
1. Clone the repository
2. Optional: Create a virtual environment
3. Install requirements
```bash
pip install -r requirements.txt
```
</details>

## Usage
<details>
<summary>Click to expand!</summary>

### Screen recording software
Screen recording software is located in `screen_recorder` folder. You can run it with `python screen_recorder.py`.

Controls:
- You can choose where to save the video. Need to enable "Save video" checkbox to save video.
- Object detection checkbox means, it will run image through a model and show on the screen with bounding boxes all the objects it detects.
- You can choose which model to use. You can choose from small, medium, large or extra-large model.
- Start recording button starts recording.
- Stop recording button stops recording.
- Choose region button lets you choose region you want to record. (Only works for main monitor)
- The slider on bottom left is confidence threshold. You can change it before and while object detection is happening on the recording to change what is the threshold of certainty the model needs to have to show an object.

### Object detection
Instructions coming soon.
</details>
