import socket
import cv2
import time
import sys
import numpy
import struct,os

IP = '127.0.0.1'
PORT = 5005
TCP_IP = '127.0.0.1'
cap = cv2.VideoCapture(0)
send = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, PORT+1))
send.connect((IP,PORT))
s.listen(1)
#res = cam.getImage().size
#socket.send(str(res[0])) #Send webcam resolution

time.sleep(1)
try:
	conn, addr = s.accept()
	conn.setblocking(False)
	while True:
		ret, frame = cap.read()
		if ret:
			encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),100]
			result, imgencode = cv2.imencode('.jpg', frame, encode_param)
			stringData = imgencode.tostring()
			try:
				#time.sleep(.0001) #otherwise send to fast and the server receive images in pieces and fail
				send.send( str(len(stringData)).ljust(16))
				send.send(stringData)
			except KeyboardInterrupt:
				send.send("quit")
				send.close()
				break
			except Exception:
				print("Error from server side")
				send.close()
				break
			decimg=cv2.imdecode(imgencode,1)
			try:
				rec = conn.recv(8)
				(x,y) = struct.unpack("ii",rec)
				print "Hand at x:",
				print x,
				print " y:",
				print y
				cv2.circle(decimg,(x,y),5,(255,255,0),3)
			except socket.error:
				pass
			cv2.imshow('CLIENT',decimg)
			if cv2.waitKey(1) & 0xFF == ord('q'):
				break
except Exception as e:
	exc_type, exc_obj, exc_tb = sys.exc_info()
	fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
	print(exc_type, fname, exc_tb.tb_lineno)
	print(e)
s.close()
send.close()
cap.release()
cv2.destroyAllWindows()
conn.close()