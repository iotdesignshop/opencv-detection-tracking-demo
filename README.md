# opencv-detection-tracking-demo
A demo using YOLOv3 and a KCF Tracker in OpenCV to automatically detect and track a soccer ball

## History
This project is based on my final assignment for the Computer Vision 1: Introduction course at OpenCV.org. I just finished up the course and enjoyed it a lot. I was pretty blown away that it's possible to write a full on object detecter and tracker in less than 200 lines of Python code, so I decided to capture that excitement in this project in case it's useful for anyone else (and to show it off a bit).

## Demonstration
This video shows the output of the demo. When a blue box is shown, the system is in "Detection" mode where is it using YOLOv3 to look for a sports ball in the frame. Once detected, the bounding box for the ball is handed off to a KCF Tracker in OpenCV and the system operates in "Tracking" mode. If tracking is lost, the system returns to "Detection" to try recover the ball position. 

It's simple, but works surpsisingly welll!

[![View on YouTube](https://github.com/iotdesignshop/opencv-detection-tracking-demo/blob/main/opencv-tracking-thumb.png?raw=true)](https://youtu.be/f0gGrJ5QMJE)

## How does it work?
What's actually going on here is pretty simple. There are two states:

1) Detection - The system is using a YOLOv3 detector to look for a high confidence detection of a "Sports Ball" in the scene. Once found, that bounding box is used to instantiate a KCF Tracker with OpenCV.
2) Tracking - The KCF Tracker is used to track the position of the ball unless it fails, at which point the system reverts back to Detection mode.

OpenCV uses the CPU for both Neural Nets and Tracking. In the Real Time video, the difference in computational load is pretty clear.... This could definitely be mitigated by switching to hardware accelerated version of YOLO, but that wasn't super important for this proof of concept.

## How can I run this myself?

Here are the basic instructions for getting it working on a Mac or Linux system. It will also run on Windows, but the procedure will be slightly different although quite similar as well as it really just relies on Python and the Python Virtual Environment system.

1) Starting point - You've got Python 3.x installed and working. If not - this is a good [tutorial as a starting point for how all that works.](https://realpython.com/python-virtual-environments-a-primer/)

2) Set up a venv for the project, and activate it
```
python3 -m venv demoenv
source demoenv/bin/activate
```

3) Install dependencies
```
pip install wheel numpy scipy matplotlib scikit-image scikit-learn ipython
pip install opencv-contrib-python
```

4) Download the YOLOv3 Weights File into the project folder - This is a couple hundred megs, so I didn't include it in the GitHub repo, but you can grab it from here:
```
wget https://pjreddie.com/media/files/yolov3.weights
```

5) Run the script
```
python tracking.py
```

Have fun!
