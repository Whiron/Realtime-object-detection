import cv2
import numpy as np
import socket
import sys
import pickle
import struct ### new code

cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',8089))
connection = clientsocket.makefile('wb')
while True:
    ret,frame=cap.read()
    data = pickle.dumps(frame) ### new code
    print(len(data))
    connection.write(struct.pack("L", len(data))+data)
