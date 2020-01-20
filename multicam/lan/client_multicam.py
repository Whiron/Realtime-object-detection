from __future__ import print_function
from imutils.video import VideoStream
from imutils.video import FPS
from realtimeobjectdetection import RealtimeObjectDetection
import base64
import cv2
import zmq
import rtsp
import time
import numpy as np
import datetime
import imutils


context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://localhost:8000')

print("[INFO] starting cameras...")
webcam1 = VideoStream(src=0).start()
webcam2 = VideoStream('rtsp://192.168.12.39:5540/ch0').start()

# initialize the two motion detectors, along with the total
# number of frames read
camMotion1 = RealtimeObjectDetection()
camMotion2 = RealtimeObjectDetection()

while True:
    frames=[]

    for (stream, motion) in zip((webcam1, webcam2), (camMotion1, camMotion2)):
        frame = stream.read()
        frame = imutils.resize(frame, width=400)
		
		# update the frames list
        frames.append(frame)
        time.sleep(0.2)
    
    for frame in frames:
        frame = cv2.resize(frame, (640, 480))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)

    # check to see if a key was pressed
    key = cv2.waitKey(1) & 0xFF
 
	# if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# do a bit of cleanup
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
webcam1.stop()
webcam2.stop()

