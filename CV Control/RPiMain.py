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
# Target Matched Variables (Controls firing)
XMatched = False
YMatched = False
#GPIO Pins UPDATE AS NEEDED
UP = 5
DOWN = 6
LEFT = 13
RIGHT = 19
FLYWHEEL = 16
BLOWER = 20

#RPi Setup
def GPIO_setup():
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(UP, GPIO.OUT)
    GPIO.setup(DOWN, GPIO.OUT)
    GPIO.setup(LEFT, GPIO.OUT)
    GPIO.setup(RIGHT, GPIO.OUT)
    GPIO.setup(FLYWHEEL, GPIO.OUT)
    GPIO.setup(BLOWER, GPIO.OUT)

# Turret Control Function

def turnTurret( direction ):
    if(direction=="stopX"):
        GPIO.output(LEFT, GPIO.LOW)   
        GPIO.output(RIGHT, GPIO.LOW)
        print("X Matched")
    elif(direction=="stopY"):
        GPIO.output(UP, GPIO.LOW)
        GPIO.output(DOWN, GPIO.LOW)
        print("Y Matched")
    else:
        if(direction=="up"):
            GPIO.output(UP, GPIO.HIGH)
            print("Moving up")
        elif(direction=="down"):
            GPIO.output(DOWN, GPIO.HIGH)
            print("Moving down")
        elif(direction=="left"):
            GPIO.output(LEFT, GPIO.HIGH)
            print("Moving left")
        elif(direction=="right"): 
            GPIO.output(RIGHT, GPIO.HIGH)
            print("Moving right")

# Turret Fire Function

def fireTurret():
    print "Firing"

# Attempt Connection to camera
cap = cv2.VideoCapture(0)
try:
    ser = serial.Serial("COM3")
    turretConnected = True
except:
    print("No Serial Connection to turret found")
    turretConnected = False

# Main Control Loop    

#GPIO_setup() #UNCOMMENT THIS LINE FOR RUNNING ON RASPBERRY PI

while(True):
    # Define variables, read screen cap
    ret, frame = cap.read()
    viewerFrame = frame
    frameCenterX = ((frame.shape[1] / 2))
    frameCenterY = ((frame.shape[0] / 2))

    # Draw Statics
    circle = cv2.circle(viewerFrame,(frameCenterX,frameCenterY), 10, (0,0,255), 1)    #Center Target
    vline = cv2.line(viewerFrame,(frameCenterX,frameCenterY+20), (frameCenterX, frameCenterY-20), (0,0,255), 2)
    hline = cv2.line(viewerFrame,(frameCenterX+20,frameCenterY), (frameCenterX-20, frameCenterY), (0,0,255), 2)
    font = cv2.FONT_HERSHEY_SIMPLEX                             #WIP
    cv2.putText(viewerFrame,'WIP v0.75',(10,450), font, .75,(255,255,255),2,cv2.LINE_AA)

    #Detect Faces

    face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_frontalface_default.xml')  
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Convert to grayscale
    faces = face_cascade.detectMultiScale(gray, 1.1, 5) #Detect faces
    for(x,y,w,h) in faces:
        cv2.rectangle(viewerFrame,(x,y),(x+w,y+h),(0,0,255),2) #Display box for viewer
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
        cv2.rectangle(viewerFrame, (Pt1X,Pt1Y),(Pt2X,Pt2Y),(139,0, 139),2) #Rectangle is hidden so it does not show up in cropped image
        print str(len(faces)) + " face(s) found"
        if (len(faces) > 0): #Detected some faces
            hand_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_hand_alt.xml')   #TODO: Trained haarcascade
            cropped = frame[Pt2Y:Pt1Y, Pt2X:Pt1X]   #Crop image to expected area where hand would be   
            if cropped.size >= 0:                                    
                grey_cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
                hands = hand_cascade.detectMultiScale(grey_cropped, 1.1, 5)      
                for (x,y,w,h) in hands:
                    cv2.rectangle(viewerFrame,(x+Pt2X,y+Pt2Y),(x+w+Pt2X,y+h+Pt2Y),(0,0,255),2)
                    if(len(hands) == 1): #1 hand found, draw target, vector and turn towards target
                        target = cv2.rectangle(viewerFrame,(x+Pt2X,y+Pt2Y),(x+w+Pt2X,y+h+Pt2Y),(0,255,0),2)
                        targetCenterX = (x+Pt2X +(w/2))
                        targetCenterY = (y+Pt2Y+(h/2))
                        targetCenterShow =  cv2.circle(viewerFrame,(targetCenterX, targetCenterY), 5, (255,255,255), -1)

                        #Draw Vector to Target
                        distanceX = frameCenterX-targetCenterX
                        cv2.putText(viewerFrame,str(distanceX),(frameCenterX-distanceX,frameCenterY-10), font, .5,(255,255,255),2,cv2.LINE_AA)
                        distanceY = frameCenterY-targetCenterY
                        cv2.putText(viewerFrame,str(distanceY),(frameCenterX-10,frameCenterY-distanceY), font, .5,(255,255,255),2,cv2.LINE_AA)
                        vector = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (targetCenterX, targetCenterY), (0,0,255), 1)
                        vectorX = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (targetCenterX, frameCenterY), (0,255,0), 1)
                        vectorY = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (frameCenterX, targetCenterY), (0,255,0), 1)
                        # Adjust X axis
                        #Negative
                        if(distanceX<-1*XMARGIN):
                            turnTurret("right")
                        #Positive
                        elif(distanceX>XMARGIN):
                            turnTurret("left")
                        #XMatched
                        else:
                            turnTurret("stopX")
                        #Adjust Y axis
                        #Negative
                        if(distanceY<-1*YMARGIN):
                            turnTurret("down")
                        #Positive
                        elif(distanceY>YMARGIN):
                            turnTurret("up")
                        else:
                            turnTurret("stopY")
                    else:
                        turnTurret("stopX")
                        turnTurret("stopY")
                print str(len(hands)) + " hand(s) found"
    cv2.imshow('Viewer', viewerFrame)
    # Key for quitting
    if cv2.waitKey(1) & 0xFF == ord('q'):
            break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


