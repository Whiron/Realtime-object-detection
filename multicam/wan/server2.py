# import required modules
from flask import Flask, render_template, Response 
import cv2
import socket 
import time
import io 
app = Flask(__name__) 

@app.route('/') 
def index(): 
   """Video streaming .""" 
   return render_template('index2.html') 
def gen(): 
   """Video streaming generator function.""" 
   while True:
      yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + open('Webcam1.jpg', 'rb').read() + b'\r\n') 
      time.sleep(0.3)

def gen2(): 
   """Video streaming generator function.""" 
   while True:
      yield (b'--frame\r\n' 
               b'Content-Type: image/jpeg\r\n\r\n' + open('Webcam2.jpg', 'rb').read() + b'\r\n') 
      time.sleep(0.3)

@app.route('/video_feed') 
def video_feed(name): 
   """Video streaming route. Put this in the src attribute of an img tag.""" 
   if (name == "Webcam1"):
      return Response(gen(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 
   if (name == "Webcam2"):
          return Response(gen2(), 
                   mimetype='multipart/x-mixed-replace; boundary=frame') 
if __name__ == '__main__': 
	app.run(host='0.0.0.0', port=80, debug=True, threaded=True) 
