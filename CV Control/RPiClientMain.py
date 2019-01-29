import Tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time 
import socket
#import RPi.GPIO as GPIO
#from USBReset import reset_USB_Device

##CONSTANTS##
#Pixel error margins
XMARGIN = 15
YMARGIN = 15  
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
UP = 17
DOWN = 27
LEFT = 22
RIGHT = 23
FLYWHEEL = 24
BLOWER = 25
#Dev variables
standalone = 1


#RPi Setup
def GPIO_setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(UP, GPIO.OUT)
    GPIO.setup(DOWN, GPIO.OUT)
    GPIO.setup(LEFT, GPIO.OUT)
    GPIO.setup(RIGHT, GPIO.OUT)
    GPIO.setup(FLYWHEEL, GPIO.OUT)
    GPIO.setup(BLOWER, GPIO.OUT)
    #Initial State Off
    GPIO.output(UP, GPIO.HIGH)
    GPIO.output(DOWN, GPIO.HIGH)
    GPIO.output(LEFT, GPIO.HIGH)
    GPIO.output(RIGHT, GPIO.HIGH)
    GPIO.output(FLYWHEEL, GPIO.HIGH)
    GPIO.output(BLOWER, GPIO.HIGH)

# Turret Control Function

def turnTurret( direction ):
    if(direction=="stopX"):
        GPIO.output(LEFT, GPIO.HIGH)   
        GPIO.output(RIGHT, GPIO.HIGH)
        print("X Matched")
    elif(direction=="stopY"):
        GPIO.output(UP, GPIO.HIGH)
        GPIO.output(DOWN, GPIO.HIGH)
        print("Y Matched")
    else:
        if(direction=="up"):
            GPIO.output(UP, GPIO.LOW)
            print("Moving up")
        elif(direction=="down"):
            GPIO.output(DOWN, GPIO.LOW)
            print("Moving down")
        elif(direction=="left"):
            GPIO.output(LEFT, GPIO.LOW)
            print("Moving left")
        elif(direction=="right"): 
            GPIO.output(RIGHT, GPIO.LOW)
            print("Moving right")

# Turret Fire Function

def fireTurret():
    GPIO.output(FLYWHEEL, GPIO.LOW)
    GPIO.output(BLOWER, GPIO.LOW)

#GPIO_setup() #UNCOMMENT THIS LINE FOR RUNNING ON RASPBERRY PI

 
class App:
    def __init__(self, window, window_title, video_source):
        self.window = window
        self.window.title(window_title)
        self.window.attributes('-fullscreen', True)
        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        self.autoMode = False


        self.frame1 = Tkinter.Frame(window)
        self.frame1.pack()
        # Fire Button
        self.btn_fire=Tkinter.Button(self.frame1, text="Fire", width=10)
        self.btn_fire.pack(side=Tkinter.LEFT, anchor=Tkinter.NW, expand=True)
        self.btn_fire.bind('<ButtonPress-1>', self.fireon)
        self.btn_fire.bind('<ButtonRelease-1>', self.fireoff)
        # Up Button
        self.btn_up=Tkinter.Button(self.frame1, text="Up", width=50)
        self.btn_up.pack(side = Tkinter.LEFT, anchor=Tkinter.N, expand=True)
        self.btn_up.bind('<ButtonPress-1>', self.up)
        self.btn_up.bind('<ButtonRelease-1>', self.y_stop)
        # Settings Button
        self.btn_settings=Tkinter.Button(self.frame1, text="Settings", width=10, command=self.settings)
        self.btn_settings.pack(side = Tkinter.LEFT, anchor=Tkinter.NE, expand=True)


        self.frame2 = Tkinter.Frame(window)
        self.frame2.pack()
        # Left Button
        self.btn_left=Tkinter.Button(self.frame2, text="Left", height=30)
        self.btn_left.pack(side=Tkinter.LEFT, anchor=Tkinter.W)
        self.btn_left.bind('<ButtonPress-1>', self.left)
        self.btn_left.bind('<ButtonRelease-1>', self.x_stop)
        # Create a canvas that can fit the above video source size
        self.canvas = Tkinter.Canvas(self.frame2, width = self.vid.width, height = 430, background='black')
        self.canvas.pack(side=Tkinter.LEFT)
        # Right Button
        self.btn_right=Tkinter.Button(self.frame2, text="Right", height=30)
        self.btn_right.pack(side=Tkinter.LEFT, anchor=Tkinter.E)
        self.btn_right.bind('<ButtonPress-1>', self.right)
        self.btn_right.bind('<ButtonRelease-1>', self.x_stop)

        self.frame3 = Tkinter.Frame(window)
        self.frame3.pack()
	# Reset Button
        self.btn_reset=Tkinter.Button(self.frame3, text="Reset Camera",command = self.resetUSB)
        self.btn_reset.pack(side = Tkinter.LEFT)
        # Down Button 
        self.btn_down=Tkinter.Button(self.frame3, text="Down", width=50)
        self.btn_down.pack(side = Tkinter.LEFT)
        self.btn_down.bind('<ButtonPress-1>', self.down)
        self.btn_down.bind('<ButtonRelease-1>', self.y_stop)
        # Mode Button
        self.btn_down=Tkinter.Button(self.frame3, text="Auto/Manual", width=10, command=self.mode)
        self.btn_down.pack(side = Tkinter.LEFT, anchor=Tkinter.E)
        

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()
    def resetUSB(self):
        #reset_USB_Device()
        if (self.video_source == 0):
            self.video_source+=1
        else:
            self.video_source = 0
        self.vid = MyVideoCapture(self.video_source)
    def down(self, event):
        turnTurret("down")
        print "Moving down"

    def y_stop(self,event):
        turnTurret("stopY")
        print "Stopping Y Movement"

    def up(self,event):
        turnTurret("up")
        print "Moving up"

    def left(self,event):
        turnTurret("left")
        print "Moving left"

    def x_stop(self,event):
        turnTurret("stopX")
        print "Stopping X Movement"

    def right(self,event):
        turnTurret("right")
        print "Moving right"

    def fireon(self,event):
        fireTurret() 
        print "Firing"
    def fireoff(self,event):
        GPIO.output(BLOWER, GPIO.HIGH)
        GPIO.output(FLYWHEEL, GPIO.HIGH)
        print "Stopping fire sequence"

    def settings(self):
        self.settingsWindow = Tkinter.Toplevel(self.window)
        self.settingsWindow.title = "Settings"
        self.sframe1 = Tkinter.Frame(self.settingsWindow)
        self.sframe1.pack()
        self.standaloneOption = Tkinter.Radiobutton(self.sframe1, text="Standalone", variable=standalone, value=1).pack()
        self.remoteOption = Tkinter.Radiobutton(self.sframe1, text="Remote Processing", variable=standalone, value=2).pack()
        self.text = Tkinter.StringVar()
        self.output = Tkinter.Label(self.sframe1, textvariable=self.text).pack()
        self.text.set("Enable PC Connection")
        self.sframe2 = Tkinter.Frame(self.settingsWindow)
        self.sframe2.pack()
        self.connectButton = Tkinter.Button(self.sframe2, text="Test Connection", command=self.connectToPC).pack(side=Tkinter.LEFT )
        self.closeButton = Tkinter.Button(self.sframe2,text="Close",command=self.closeSettings).pack( side=Tkinter.LEFT )

    def connectToPC(self):
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5005
        BUFFER_SIZE = 1024
        MESSAGE = "Hello, PC!"

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        data = s.recv(BUFFER_SIZE)
        s.close()

        self.text.set(data)

    def closeSettings(self):
        self.settingsWindow.destroy()

    def detectFaces(self, frame):
        if standalone == 1:
            frameCenterX = ((frame.shape[1] / 2))
            frameCenterY = ((frame.shape[0] / 2))
            
            # Draw Statics
            font = cv2.FONT_HERSHEY_SIMPLEX
            #circle = cv2.circle(frame,(frameCenterX,frameCenterY), 2, (0,0,255), 1)    #Center Target
            #vline = cv2.line(frame,(frameCenterX,frameCenterY+5), (frameCenterX, frameCenterY-5), (0,0,255), 2)
            #hline = cv2.line(frame,(frameCenterX+5,frameCenterY), (frameCenterX-5, frameCenterY), (0,0,255), 2)
            hand_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_hand_alt.xml')   #TODO: Trained haarcascade  
            face_cascade = cv2.CascadeClassifier('/home/pi/opencv-3.4.3/data/haarcascades/haarcascade_frontalface_default.xml')  
            gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY) #Convert to grayscale
            faces = face_cascade.detectMultiScale(gray, 1.1, 5) #Detect faces
            for(x,y,w,h) in faces:
                #cv2.rectangle(frame,(x,y),(x+w,y+h),(0,0,255),2) #Display box for viewer  
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
                            #targetCenterShow =  cv2.circle(frame,(targetCenterX, targetCenterY), 5, (255,255,255), -1)

                            #Draw Vector to Target
                            distanceX = frameCenterX-targetCenterX
                            #cv2.putText(frame,str(distanceX),(frameCenterX-distanceX,frameCenterY-10), font, .5,(255,255,255),2,cv2.LINE_AA)
                            distanceY = frameCenterY-targetCenterY
                            #cv2.putText(frame,str(distanceY),(frameCenterX-10,frameCenterY-distanceY), font, .5,(255,255,255),2,cv2.LINE_AA)
                            #vector = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (targetCenterX, targetCenterY), (0,0,255), 1)
                            #vectorX = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (targetCenterX, frameCenterY), (0,255,0), 1)
                            #vectorY = cv2.arrowedLine(frame, (frameCenterX, frameCenterY), (frameCenterX, targetCenterY), (0,255,0), 1)    
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
                            return True
                        else:
                            print "No hands found"
                            return False
            else:
                print "More than one face found"
                return False
        else:
            pass

    def mode(self):    
        self.autoMode = not self.autoMode
        print "autoMode is " + str(self.autoMode)
        
        
    def update(self):
        #try:
        
            # Get a frame from the video source
            ret, frame = self.vid.get_frame()

            if ret:
                if self.autoMode:
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    cv2.putText(frame, 'AUTO', (50,70), font, .75, (255,0,0),2,cv2.LINE_AA)
                    imageResize = cv2.resize(frame, None, fx = 0.65, fy = 0.65)
                    if not (self.detectFaces(imageResize)):
                        turnTurret("stopX")
                        turnTurret("stopY")
                    self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(imageResize))
                    self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, image = self.photo, anchor = Tkinter.CENTER)
                else:
                    self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                    self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, image = self.photo, anchor = Tkinter.CENTER)
        #except:
            self.window.after(self.delay, self.update)
        

class MyVideoCapture:
    def __init__(self, video_source):
       # Open the video source
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        # Get video source width and height
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

# Create a window and pass it to the Application object
App(Tkinter.Tk(), "Tkinter and OpenCV", 0)
