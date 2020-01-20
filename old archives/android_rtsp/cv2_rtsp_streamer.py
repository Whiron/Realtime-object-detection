import base64
from imutils.video import FPS
import cv2
import zmq
import rtsp
import time

context = zmq.Context()
footage_socket = context.socket(zmq.PUB)
footage_socket.connect('tcp://18.218.149.252:8000')

camera = cv2.VideoCapture('rtsp://192.168.12.39:5540/ch0')  # init the camera
fps = FPS().start()

while True:
    try:
        grabbed, frame = camera.read()  # grab the current frame
        frame = cv2.resize(frame, (640, 480))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', frame)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket.send(jpg_as_text)
        fps.update()

    except KeyboardInterrupt:
        fps.stop()
        # print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
        print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
        camera.release()
        cv2.destroyAllWindows()
        break