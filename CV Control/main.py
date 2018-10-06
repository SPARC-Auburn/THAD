import numpy as np
import cv2
import serial
import sys
import time

cap = cv2.VideoCapture(0)
try:
    ser = serial.Serial("COM3")
except:
    print("No Serial Connection to turret found")
#cap.capture(stream, format='jpeg')
while(True):
##### Capture frame-by-frame
    ret, frame = cap.read()
    frameCenterX = (frame.shape[1] / 2)
    frameCenterY = (frame.shape[0] / 2)
##### Drawing Static Images
    circle = cv2.circle(frame,(frameCenterX,frameCenterY), 10, (0,0,255), 1)    #Center Target
    vline = cv2.line(frame,(frameCenterX,frameCenterY+20), (frameCenterX, frameCenterY-20), (0,0,255), 2)
    hline = cv2.line(frame,(frameCenterX+20,frameCenterY), (frameCenterX-20, frameCenterY), (0,0,255), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX                             #WIP
    cv2.putText(frame,'WIP',(10,450), font, 1,(255,255,255),2,cv2.LINE_AA)

###### TEST: DETECT FACE #####  
    face_cascade = cv2.CascadeClassifier('C:\Users\joshj\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')   
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 5) #Detect faces
    print "Found "+str(len(faces))+" face(s)"

    #Display potential faces

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)

###### Detect human poses

     #Display them

###### TEST: DETERMINE IF OBJECT IS VALID TARGET #####
    targetFound = False
    if (len(faces) == 1):   #One face only ###TODO: MORE FACES
        targetFound = True
        for (x,y,w,h) in faces:
            target = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
            targetCenter = (x+w/2), (y+h/2)
            targetCenterShow =  cv2.circle(frame,targetCenter, 5, (255,255,255), -1)

###### Detect a certain pose

     #Recolor correct pose

###### TEST: MOVE OBJECT CENTER TO FRAME CENTER USING SERIAL CONNECTION #####

     # Loop to check and adjust until center is within error range
    if(targetFound):
         vector = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (targetCenter), (0,0,255), 1)
     # If object can't be found, break the loop

###### Try to move the pose center to the frame center (close to it) 

###### Display the resulting frame
    cv2.imshow('frame',circle)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()