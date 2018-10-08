import numpy as np
import cv2
import serial
import sys
import time
##CONSTANTS##
#Pixel error margins
XMARGIN = 10
YMARGIN = 10  
#Camera position offsets
OFFSETX = 0
OFFSETY = 0
###


cap = cv2.VideoCapture(0)
try:
    ser = serial.Serial("COM3")
    connected = True
except:
    print("No Serial Connection to turret found")
    connected = False
#cap.capture(stream, format='jpeg')
while(True):
##### Capture frame-by-frame
    ret, frame = cap.read()
    frameCenterX = ((frame.shape[1] / 2) + OFFSETX)
    frameCenterY = ((frame.shape[0] / 2) + OFFSETY)
##### Drawing Static Images
    circle = cv2.circle(frame,(frameCenterX,frameCenterY), 10, (0,0,255), 1)    #Center Target
    vline = cv2.line(frame,(frameCenterX,frameCenterY+20), (frameCenterX, frameCenterY-20), (0,0,255), 2)
    hline = cv2.line(frame,(frameCenterX+20,frameCenterY), (frameCenterX-20, frameCenterY), (0,0,255), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX                             #WIP
    cv2.putText(frame,'WIP v0.5',(10,450), font, .75,(255,255,255),2,cv2.LINE_AA)

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
            targetCenterX = (x+w/2)
            targetCenterY = (y+h/2)
            targetCenterShow =  cv2.circle(frame,(targetCenterX, targetCenterY), 5, (255,255,255), -1)

###### Detect a certain pose

     #Recolor correct pose

###### TEST: MOVE OBJECT CENTER TO FRAME CENTER USING SERIAL CONNECTION #####

     # Check and adjust until center is within error range
    if(targetFound):
        vector = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (targetCenterX, targetCenterY), (0,0,255), 1)
        vectorX = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (targetCenterX, frameCenterY), (0,255,0), 1)
        vectorY = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (frameCenterX, targetCenterY), (0,255,0), 1)


###### Try to move the pose center to the frame center (close to it) 
        distanceX = frameCenterX-targetCenterX
        cv2.putText(frame,str(distanceX),(frameCenterX-distanceX,frameCenterY-10), font, .5,(255,255,255),2,cv2.LINE_AA)
        distanceY = frameCenterY-targetCenterY
        cv2.putText(frame,str(distanceY),(frameCenterX-10,frameCenterY-distanceY), font, .5,(255,255,255),2,cv2.LINE_AA)
        if(connected):
            #Vector to target
            #Adjust X axis
            #Negative
            if(distanceX<-1*XMARGIN):
                ser.write('d')  #Move right
                ser.write('f')  #Stop moving left
                print("Moving right")
            #Positive
            elif(distanceX>XMARGIN):
                ser.write('a')  #Move left
                ser.write('h')  #Stop moving right
                print("Moving left")
            else:
                ser.write('f')  #Stop all
                ser.write('h')
                print("X matched")
            #Adjust Y axis
            #Negative
            if(distanceY<-1*YMARGIN):
                ser.write('s')  #Move down
                ser.write('t')  #Stop moving up
                print("Moving down")
            #Positive
            elif(distanceY>YMARGIN):
                ser.write('w')  #Move up
                ser.write('g')  #Stop moving down
                print("Moving up")
            else:
                ser.write('t')  #Stop all
                ser.write('g')
                print("Y matched")
        else:
            print("Found target- but not connected to turret")
    else:   #Valid target not found- stop turret
        if(connected):
            ser.write('t')
            ser.write('g')
            ser.write('h')
            ser.write('f')

###### Display the resulting frame
    cv2.imshow('frame',circle)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        if(connected):  #Stop turret
            ser.write('t')
            ser.write('g')
            ser.write('h')
            ser.write('f')
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()