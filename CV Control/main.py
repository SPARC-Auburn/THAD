import numpy as np
import cv2
import serial
import sys
import time
import math
##CONSTANTS##
#Pixel error margins
XMARGIN = 30
YMARGIN = 30  
#Camera position offsets
OFFSETX = 0
OFFSETY = 0
Pt1Y = 0
Pt2Y = 0
Pt2X = 0
Pt1X = 0
###


cap = cv2.VideoCapture(0)
try:
    ser = serial.Serial("COM3")
    connected = True
except:
    print("No Serial Connection to turret found")
    connected = False
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

##### Detect Faces
    face_cascade = cv2.CascadeClassifier('C:\Users\joshj\Downloads\opencv\sources\data\haarcascades\haarcascade_frontalface_default.xml')  
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 5) #Detect faces

    #Detect Hands
    #Define search space for hands based on face detection and size of face
    for(x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2)
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
    #Try to find hands in search frame using contour detection
    hand_cascade = cv2.CascadeClassifier('C:\Users\joshj\Downloads\opencv\sources\data\haarcascades\haarcascade_hand_alt.xml')   #TODO: Trained haarcascade
    cropped = frame[Pt2Y:Pt1Y, Pt2X:Pt1X]   #Crop image to expected area where hand would be                                       
    grey_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    hands = hand_cascade.detectMultiScale(grey_cropped, 1.1, 5)      
    for (x,y,w,h) in hands:
        cv2.rectangle(frame,(x+Pt2X,y+Pt2Y),(x+w+Pt2X,y+h+Pt2Y),(0,0,255),2)
        print "(" + str(x-Pt2X) + "," + str(y-Pt2Y) +")"
    cv2.imshow('gray_crop',grey_cropped)
    print "Found "+str(len(faces))+" face(s)" +str(len(hands))+" hand(s)"
    #Display potential objects

##### Determine if pose is valid
    targetFound = False
    if (len(hands) == 1):   #Detect if there is one valid hand                                                                  
        targetFound = True
        for (x,y,w,h) in hands:
            target = cv2.rectangle(frame,(x+Pt2X,y+Pt2Y),(x+w+Pt2X,y+h+Pt2Y),(0,255,0),2)
            targetCenterX = (x+Pt2X +(w/2))
            targetCenterY = (y+Pt2Y+(h/2))
            targetCenterShow =  cv2.circle(frame,(targetCenterX, targetCenterY), 5, (255,255,255), -1)

##### Move object center using serial connection

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