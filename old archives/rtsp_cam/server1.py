# import the necessary packages
#from imutils.video import VideoStream
#from imutils.video import pivideostream
from imutils.video import __init__
from imutils.video import FPS
from multiprocessing import Process
from multiprocessing import Queue
from flask import Flask, render_template, Response 
from PIL import Image
from numpy import array
import io
import socket
import cv2
import struct
import datetime
import argparse
import imutils
import time
import numpy as np 

def classify_frame(net, inputQueue, outputQueue):
	# keep looping
	while True:
		# check to see if there is a frame in our input queue
		if not inputQueue.empty():
			# grab the frame from the input queue, resize it, and
			# construct a blob from it
			#time.sleep(5.0)
			#inputQueue.clean()
			frame = inputQueue.get()
			frame = cv2.resize(frame, (300, 300))
			blob = cv2.dnn.blobFromImage(frame, 0.007843,
				(300, 300), 127.5)

			# set the blob as input to our deep learning object
			# detector and obtain the detections
			net.setInput(blob)
			detections = net.forward()

			# write the detections to the output queue
			outputQueue.put(detections)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-p", "--prototxt", default = "MobileNetSSD_deploy.prototxt.txt",
	help="path to Caffe 'deploy' prototxt file")
ap.add_argument("-m", "--model", default = "MobileNetSSD_deploy.caffemodel",
	help="path to Caffe pre-trained model")
ap.add_argument("-c", "--confidence", type=float, default=0.2,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "Human", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]
COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))


# load our serialized model from disk
print("[INFO] loading model...")
net = cv2.dnn.readNetFromCaffe(args["prototxt"], args["model"])

# initialize the input queue (frames), output queue (detections),
# and the list of actual detections returned by the child process
inputQueue = Queue(maxsize=1)
outputQueue = Queue(maxsize=1)
detections = None

# print("[INFO] starting flask...")
# f = Process(target=flask_server, args=())
# f.daemon = True
# f.start()

# construct a child process *indepedent* from our main process of
# execution
print("[INFO] starting process...")
p = Process(target=classify_frame, args=(net, inputQueue,
	outputQueue,))
p.daemon = True
p.start()


# Start a socket listening for connections on 0.0.0.0:8000 (0.0.0.0 means
# all interfaces)
# client_socket = socket.socket()
# client_socket.connect(('localhost', 5001))
# connection2 = client_socket.makefile('wb')
# stream = io.BytesIO()

server_socket = socket.socket()
server_socket.bind(('0.0.0.0', 8000))
server_socket.listen(0)

# Accept a single connection and make a file-like object out of it
connection = server_socket.accept()[0].makefile('rb')
try:
	while True:
		#time.sleep(0.3)
		# Read the length of the image as a 32-bit unsigned int. If the
		# length is zero, quit the loop
		image_len = struct.unpack('<L', connection.read(struct.calcsize('<L')))[0]
		if not image_len:
			break
		# Construct a stream to hold the image data and read the image
		# data from the connection
		image_stream = io.BytesIO()
		image_stream.write(connection.read(image_len))
		# Rewind the stream, open it as an image with PIL and do some
		# processing on it
		image_stream.seek(0)
		image = Image.open(image_stream).convert('RGB')
		
		# Convert Image to NumPy Array for processing
		arr=array(image)
		arr=imutils.resize(arr,width=400)

		# Create a frame
		#cv2.resizeWindow('frame',800,800)
		np_frame = np.array(image)
		print(np_frame.shape)
		# Add time stamp
		timestamp= datetime.datetime.now()
		ts=timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
		#cv2.putText(arr,ts, (10, arr	.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX,0.35,(0,0,255),1)

		# Display Stream
		frame=cv2.cvtColor(np_frame,cv2.COLOR_RGB2BGR) # CV Image
		print(frame.shape)
		key=cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break
		print(type(arr))
		print('Image is', image)
		image.verify()
		#print('Image is verified')

		# Process Image
		frame = imutils.resize(frame, width=400)
		(fH, fW) = frame.shape[:2]

		# if the input queue *is* empty, give the current frame to
		# classify
		if inputQueue.empty():
			inputQueue.put(frame)
			#inputQueue.queue.clear()

		# if the output queue *is not* empty, grab the detections
		if not outputQueue.empty():
			detections = outputQueue.get()
		

		# check to see if our detectios are not None (and if so, we'll
		# draw the detections on the frame)
		if detections is not None:
			# loop over the detections
			for i in np.arange(0, detections.shape[2]):
				# extract the confidence (i.e., probability) associated
				# with the prediction
				confidence = detections[0, 0, i, 2]
	
				# filter out weak detections by ensuring the `confidence`
				# is greater than the minimum confidence
				if confidence < args["confidence"]:
					continue

				# otherwise, extract the index of the class label from
				# the `detections`, then compute the (x, y)-coordinates
				# of the bounding box for the object
				idx = int(detections[0, 0, i, 1])
				dims = np.array([fW, fH, fW, fH])
				box = detections[0, 0, i, 3:7] * dims
				(startX, startY, endX, endY) = box.astype("int")
	
				# draw the prediction on the frame
				label = "{}: {:.2f}%".format(CLASSES[idx],
					confidence * 100)
				cv2.rectangle(frame, (startX, startY), (endX, endY),
					COLORS[idx], 2)
				y = startY - 15 if startY - 15 > 15 else startY + 15
				cv2.putText(frame, label, (startX, y),
					cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)
	
		# Final Strem
		cv2.imwrite('pic.jpg', frame)
		#time.sleep(0.3)
		key=cv2.waitKey(1) & 0xFF
		if key == ord("q"):
			break 
finally:
	connection.close()
	server_socket.close()

