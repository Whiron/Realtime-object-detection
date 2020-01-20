import io
import socket
import struct
import time
import cv2
import pickle
# Connect a client socket to my_server:8000 (change my_server to the
# hostname of your server)
client_socket = socket.socket()
client_socket.connect(('localhost', 8000))

# Make a file-like object out of the connection
connection = client_socket.makefile('wb')
try:
        # with picamera.PiCamera() as camera:
        #     camera.resolution = (400,400)
        #     camera.exposure_mode='night'
        #     camera.rotation='180'
        #     # Start a preview and let the camera warm up for 2 seconds
        #     camera.start_preview()
        #     time.sleep(2)
        camera=cv2.VideoCapture(0)       

        # Note the start time and construct a stream to hold image data
        # temporarily (we could write it directly to connection but in this
        # case we want to find out the size of each capture first to keep
        # our protocol simple)
        start = time.time()
        stream = io.BytesIO()
        while True:
            ret, frame=camera.read()
            data = pickle.dumps(frame) ### new code
            # Write the length of the capture to the stream and flush to
            # ensure it actually gets sent
            connection.write(struct.pack("<L", len(data)))
            connection.flush()
            # Rewind the stream and send the image data over the wire
            stream.seek(0)
            connection.write(data)
            # stream.seek(0)
            # print(stream.read())
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

