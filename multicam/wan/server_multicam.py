import cv2
import zmq
import base64
import numpy as np
import threading
import datetime
from realtimeobjectdetection import RealtimeObjectDetection

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket.bind('tcp://*:8000')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
count=0
frames=[]
camMotion1 = RealtimeObjectDetection()
camMotion2 = RealtimeObjectDetection()
while True:
    
    try:
        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)
        frames.append(source)
        count=count+1
        print ("frame recived",count)
        print ("length of array",len(frames))
        if(count % 2 == 0):
            # loop over the frames a second time
            for (frame, name,motion) in zip(frames, ("Webcam1", "Webcam2"),(camMotion1, camMotion2)):
                frame = motion.update(frame)
                timestamp = datetime.datetime.now()
                ts = timestamp.strftime("%A %d %B %Y %I:%M:%S%p")
                # draw the timestamp on the frame and display it
                cv2.putText(frame,ts, (10, frame.shape[0] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
                #cv2.imshow(name, frame)
                cv2.imwrite(name+'.jpg', frame)
                count = 0
                frames=[]
                
        
            # check to see if a key was pressed
            key = cv2.waitKey(1) & 0xFF
        
            # if the `q` key was pressed, break from the loop
            if key == ord("q"):
                break

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break