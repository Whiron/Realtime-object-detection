import cv2
import numpy as np
import socket
import sys
import pickle
import struct
import io
import imutils
import time

# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('localhost',8000))

#camera
cap = cv2.VideoCapture("rtsp://root:pass@192.168.12.39:5540/ch0")

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
    start = time.time()
    stream = io.BytesIO()
    while True:
        ret, frame = cap.read()
        stream = cv2.imencode('.jpg', frame)
        print (stream)
        print (len(stream))
        # for foo in camera.capture_continuous(stream,'jpeg'):
        # Write the length of the capture to the stream and flush to
        # ensure it actually gets sent
        connection.write(struct.pack('<L', len(stream)))
        connection.flush()
        # Rewind the stream and send the image data over the wire
        stream.seek(0)
        connection.write(stream)
        # If we've been capturing for more than 30 seconds, quit
        if time.time() - start > 18000000000:
            break
        # Reset the stream for the next capture
        stream.seek(0)
        stream.truncate()
    # Write a length of zero to the stream to signal we're done
    connection.write(struct.pack('<L', 0))
finally:
    connection.close()
    client_socket.close()

