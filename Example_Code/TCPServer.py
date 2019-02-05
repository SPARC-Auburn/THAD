#!/usr/bin/env python
 
import socket
import numpy
import cv2

TCP_IP = '127.0.0.1'
TCP_PORT = 5005
def detectFaces(frame):
    frameCenterX = ((frame.shape[1] / 2))
    frameCenterY = ((frame.shape[0] / 2))
            
            # Draw Statics
    font = cv2.FONT_HERSHEY_SIMPLEX
    circle = cv2.circle(frame,(frameCenterX,frameCenterY), 2, (0,0,255), 1)    #Center Target
    vline = cv2.line(frame,(frameCenterX,frameCenterY+5), (frameCenterX, frameCenterY-5), (0,0,255), 2)
    hline = cv2.line(frame,(frameCenterX+5,frameCenterY), (frameCenterX-5, frameCenterY), (0,0,255), 2)
    hand_cascade = cv2.CascadeClassifier('C:\Users\joshj\Downloads\opencv\sources\data\haarcascades\haarcascade_hand_alt.xml')   #TODO: Trained haarcascade  
    face_cascade = cv2.CascadeClassifier('C:\Users\joshj\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')  
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 5) #Detect faces
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2) #Display box for viewer  
        print str(len(faces)) + " face(s) found"
        if (len(faces)== 1): #Detected 1 face and in standalone mode
            Pt1X = x-w #Tuned constants for rough area of arm location based on size of face 
            if Pt1X < 20: #Must be positive
                Pt1X = 20
            Pt1Y = y+h
            if Pt1Y < 20:
                Pt1Y = 20
            Pt2X = x-(3*w)
            if Pt2X < 10:
                Pt2X = 10
            Pt2Y = y-h
            if Pt2Y < 10:
                Pt2Y = 10
            cv2.rectangle(frame, (Pt1X,Pt1Y),(Pt2X,Pt2Y),(139,0, 139),2) #Rectangle is hidden so it does not show up in cropped image
            cropped = frame[Pt2Y:Pt1Y, Pt2X:Pt1X]   #Crop image to expected area where hand would be   
            if cropped.size >= 0:                                    
                grey_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                hands = hand_cascade.detectMultiScale(grey_cropped, 1.1, 5)      
                for (x,y,w,h) in hands:
                    cv2.rectangle(frame,(x+Pt2X,y+Pt2Y),(x+w+Pt2X,y+h+Pt2Y),(0,0,255),2)
                    if(len(hands) == 1): #1 hand found, draw target, vector and turn towards target
                        print "Target found!"
                        target = cv2.rectangle(frame,(x+Pt2X,y+Pt2Y),(x+w+Pt2X,y+h+Pt2Y),(0,255,0),2)
                        targetCenterX = (x+Pt2X +(w/2))
                        targetCenterY = (y+Pt2Y+(h/2))
                        targetCenterShow =  cv2.circle(frame,(targetCenterX, targetCenterY), 5, (255,255,255), -1)

                        #Draw Vector to Target
                        distanceX = frameCenterX-targetCenterX
                        cv2.putText(frame,str(distanceX),(frameCenterX-distanceX,frameCenterY-10), font, .5,(255,255,255),2,cv2.LINE_AA)
                        distanceY = frameCenterY-targetCenterY
                        cv2.putText(frame,str(distanceY),(frameCenterX-10,frameCenterY-distanceY), font, .5,(255,255,255),2,cv2.LINE_AA)
                        vector = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (targetCenterX, targetCenterY), (0,0,255), 1)
                        vectorX = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (targetCenterX, frameCenterY), (0,255,0), 1)                            #vectorY = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (frameCenterX, targetCenterY), (0,255,0), 1)  

def recvall(sock, count):
    buf = b''
    while count:
        newbuf = sock.recv(count)
        if not newbuf: return None
        buf += newbuf
        count -= len(newbuf)
    return buf

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((TCP_IP, TCP_PORT))
s.listen(1)
while 1:
    conn, addr = s.accept()
    print 'Connection address:', addr
    while 1:
        length = recvall(conn,16)
        stringData = recvall(conn, int(length))
        data = numpy.fromstring(stringData, dtype='uint8')
        decimg=cv2.imdecode(data,1)
        detectFaces(decimg)
        cv2.imshow('SERVER',decimg)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    conn.close()
cap.release()
cv2.destroyAllWindows()