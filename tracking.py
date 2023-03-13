import numpy as np
import cv2,os


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i - 1] for i in net.getUnconnectedOutLayers()]


# Remove the bounding boxes with low confidence using non-maxima suppression
def postprocess(frame, outs):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    classIds = []
    confidences = []
    boxes = []
    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []

    # We are only inteested in the "sports ball" class
    sportsBallClassId = classes.index("sports ball")

    for out in outs:
        for detection in out:
            if detection[4] > objectnessThreshold :
                scores = detection[5:]
                classId = np.argmax(scores)
                confidence = scores[classId]
                if (confidence > confThreshold) and (classId == sportsBallClassId):
                    center_x = int(detection[0] * frameWidth)
                    center_y = int(detection[1] * frameHeight)
                    width = int(detection[2] * frameWidth)
                    height = int(detection[3] * frameHeight)
                    left = int(center_x - width / 2)
                    top = int(center_y - height / 2)
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

    if (len(indices) > 0):
        # Return the first result
        box = boxes[0]
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        
        return (left, top, width, height)
    else:
        return None
    
    


# YOLO parameters
objectnessThreshold = 0.5 # Objectness threshold
confThreshold = 0.5       # Confidence threshold
nmsThreshold = 0.4        # Non-maximum suppression threshold
inpWidth = 416            # Width of network's input image
inpHeight = 416           # Height of network's input image

# Load names of classes
classesFile = "coco.names"
classes = None
with open(classesFile, 'rt') as f:
    classes = f.read().rstrip('\n').split('\n')

# Give the configuration and weight files for the model and load the network using them.
modelConfiguration = "yolov3.cfg"
modelWeights = "yolov3.weights"

net = cv2.dnn.readNetFromDarknet(modelConfiguration, modelWeights)

# Process inputs
videoPath = "soccer-ball.mp4"

# Open the video file
cap = cv2.VideoCapture(videoPath)

# Read the first frame
hasFrame, frame = cap.read()

# Mode string
mode = "Detecting"
state = "Tracking not started"

# Detected bounding box
ballBoundingBox = None

while hasFrame:

    if (mode == "Detecting"):
        # Create a 4D blob from a frame.
        blob = cv2.dnn.blobFromImage(frame, 1/255, (inpWidth, inpHeight), [0,0,0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outs = net.forward(getOutputsNames(net))
        
        # Remove the bounding boxes with low confidence
        ballBoundingBox = postprocess(frame, outs)
        if (ballBoundingBox != None):
            # Draw a blue bounding box to indicate detection mode
            p1 = (ballBoundingBox[0], ballBoundingBox[1])
            p2 = (ballBoundingBox[0] + ballBoundingBox[2], ballBoundingBox[1] + ballBoundingBox[3])
            cv2.rectangle(frame, p1, p2, (255, 178, 50), 3)

            # Initialize tracker with frame and bounding box
            tracker = cv2.TrackerKCF_create()
            tracker.init(frame, ballBoundingBox)

            # Switch to tracking mode
            mode = "Tracking"
            state = "Tracking started"

            # Display the frame
            cv2.imshow("frame", frame)

            cv2.waitKey(0)
            

    else:
        # Tracking mode
        
        # Update tracker
        success, ballBoundingBox = tracker.update(frame)

        if(success):
            # Tracking success
            state = "Tracking success"
            # Draw bounding box
            p1 = (int(ballBoundingBox[0]), int(ballBoundingBox[1]))
            p2 = (int(ballBoundingBox[0] + ballBoundingBox[2]), int(ballBoundingBox[1] + ballBoundingBox[3]))
            cv2.rectangle(frame, p1, p2, (0, 255, 0), 3)
        else :
            # Tracking failure
            state = "Tracking failure"
            mode = "Detecting"
            tracker = None
            

    # Draw a black box behind text
    cv2.rectangle(frame, (0, 0), (300, 40), (0, 0, 0), cv2.FILLED)
    cv2.putText(frame, "Mode: "+mode, (0, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

    color = (255,255,255)
    if ("failure" in state):
        color = (0, 0, 255)

    cv2.putText(frame, "State: "+state, (0, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color)


    # Display the frame
    cv2.imshow("frame", frame)

     # Check for escape key
    key = cv2.waitKey(1)
    if key == 27:
        break

    # Read the next frame
    hasFrame, frame = cap.read()

    
# Close the video file
cap.release()

# Close all windows
cv2.destroyAllWindows()