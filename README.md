# opencv-detection-tracking-demo
A demo using YOLOv3 and a KCF Tracker in OpenCV to automatically detect and track a soccer ball

## History
This project is based on my final assignment for the Computer Vision 1: Introduction course at OpenCV.org. I just finished up the course and enjoyed it a lot. I was pretty blown away that it's possible to write a full on object detecter and tracker in less than 200 lines of Python code, so I decided to capture that excitement in this project in case it's useful for anyone else (and to show it off a bit).

## Demonstration
This video shows the output of the demo. When a blue box is shown, the system is in "Detection" mode where is it using YOLOv3 to look for a sports ball in the frame. Once detected, the bounding box for the ball is handed off to a KCF Tracker in OpenCV and the system operates in "Tracking" mode. If tracking is lost, the system returns to "Detection" to try recover the ball position. 

It's simple, but works surpsisingly welll!

[![View on YouTube](https://github.com/iotdesignshop/opencv-detection-tracking-demo/blob/main/opencv-tracking-thumb.png?raw=true)](https://youtu.be/f0gGrJ5QMJE)
