from socket import *
import cv2
import time
import sys
import numpy

IP = '127.0.0.1'
PORT = 5005

cap = cv2.VideoCapture(0)
socket = socket(AF_INET,SOCK_STREAM)
socket.connect((IP,PORT))
#res = cam.getImage().size
#socket.send(str(res[0])) #Send webcam resolution

time.sleep(1)

while True:
	ret, frame = cap.read()
	if ret:
		encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),100]
		result, imgencode = cv2.imencode('.jpg', frame, encode_param)
		stringData = imgencode.tostring()
		try:
			time.sleep(.0001) #otherwise send to fast and the server receive images in pieces and fail
			socket.send( str(len(stringData)).ljust(16))
			socket.send(stringData)
		except KeyboardInterrupt:
			socket.send("quit")
			socket.close()
			break
		except Exception:
			print("Error from server side")
			socket.close()
			break
		decimg=cv2.imdecode(imgencode,1)
		cv2.imshow('CLIENT',decimg)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
cap.release()
cv2.destroyAllWindows()