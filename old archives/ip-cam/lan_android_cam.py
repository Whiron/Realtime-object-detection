import requests
import cv2
import numpy as np

url = "http://10.162.119.219:8080/shot.jpg"

while True:

	img_resp=requests.get(url)
	img_arr = np.array(bytearray(img_resp.content),dtype=np.uint8)
	img = cv2.imdecode(img_arr, -1)
	cv2.imshow("Android_Cam",img)
	
	key=cv2.waitKey(1) & 0xFF
	if key == ord("q"):
		break  
