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
s.listen(1)
conn, addr = s.accept()
send.connect((addr[0],PORT))

#res = cam.getImage().size
#socket.send(str(res[0])) #Send webcam resolution

time.sleep(1)
try:
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
				rec = conn.recv(4*12)
				(fx,fy,fw,fh,sx,sy,sw,sh,hx,hy,hw,hh) = struct.unpack("iiiiiiiiiiii",rec)
				if fx >= 0:
					cv2.rectangle(frame,(fx,fy),(fx+fw,fy+fh),(0,0,255),3)
					cv2.rectangle(frame,(sx,sy),(sx+sw,sy+sh),(255,0,255),3)
					if hx >= 0:
						cv2.rectangle(frame,(hx,hy),(hx+hw,hy+hh),(0,255,0),3)
			except socket.error:
				pass
			cv2.imshow('CLIENT',frame)	
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