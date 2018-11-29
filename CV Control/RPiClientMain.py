import Tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time 
#import RPi.GPIO as GPIO

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
UP = 17
DOWN = 27
LEFT = 22
RIGHT = 23
FLYWHEEL = 24
BLOWER = 25
#Dev variables

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
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
       # self.window.attributes('-fullscreen', True)
        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)
        self.autoMode = True
        self.frame1 = Tkinter.Frame(window)
        self.frame1.pack(fill=Tkinter.BOTH)
        # Fire Button
        self.btn_fire=Tkinter.Button(self.frame1, text="Fire", width=10, height = 1)
        self.btn_fire.pack(side=Tkinter.LEFT, anchor=Tkinter.NW, expand=True)
        self.btn_fire.bind('<ButtonPress-1>', self.fireon)
        self.btn_fire.bind('<ButtonRelease-1>', self.fireoff)
        # Up Button
        self.btn_up=Tkinter.Button(self.frame1, text="Up", width=50, height = 1)
        self.btn_up.pack(side = Tkinter.LEFT, anchor=Tkinter.N, expand=True)
        self.btn_up.bind('<ButtonPress-1>', self.up)
        self.btn_up.bind('<ButtonRelease-1>', self.y_stop)
        # Settings Button
        self.btn_settings=Tkinter.Button(self.frame1, text="Settings", width=10, height = 1, command=self.settings)
        self.btn_settings.pack(side = Tkinter.LEFT, anchor=Tkinter.NE, expand=True)


        self.frame2 = Tkinter.Frame(window)
        self.frame2.pack(fill=Tkinter.X, expand = True)
        # Left Button
        self.btn_left=Tkinter.Button(self.frame2, text="Left", width=10, height = 50)
        self.btn_left.pack(side=Tkinter.LEFT, anchor=Tkinter.E)
        self.btn_left.bind('<ButtonPress-1>', self.left)
        self.btn_left.bind('<ButtonRelease-1>', self.x_stop)
        # Create a canvas that can fit the above video source size
        self.canvas = Tkinter.Canvas(self.frame2, width = self.vid.width, height = self.vid.height, background='black')
        self.canvas.pack(side=Tkinter.LEFT, fill=Tkinter.BOTH)
        # Right Button
        self.btn_right=Tkinter.Button(self.frame2, text="Right", width=10, height=50)
        self.btn_right.pack(side=Tkinter.LEFT, anchor=Tkinter.W, expand=False)
        self.btn_right.bind('<ButtonPress-1>', self.right)
        self.btn_right.bind('<ButtonRelease-1>', self.x_stop)

        self.frame3 = Tkinter.Frame(window)
        self.frame3.pack(fill=Tkinter.BOTH)
        # Down Button 
        self.btn_down=Tkinter.Button(self.frame3, text="Down", width=50, height = 20)
        self.btn_down.pack(side = Tkinter.BOTTOM, expand=True)
        self.btn_down.bind('<ButtonPress-1>', self.down)
        self.btn_down.bind('<ButtonRelease-1>', self.y_stop)
        # Mode Button
        self.btn_down=Tkinter.Button(self.frame3, text="Auto/Manual", width=50, height = 20, command=self.mode)
        self.btn_down.pack(side = Tkinter.RIGHT, anchor=Tkinter.W, expand=True)
        

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def down(self, event):
        #turnTurret("down")
        print "Moving down"

    def y_stop(self,event):
        #turnTurret("stopY")
        print "Stopping Y Movement"

    def up(self,event):
        #turnTurret("up")
        print "Moving up"

    def left(self,event):
        #turnTurret("left")
        print "Moving left"

    def x_stop(self,event):
        #turnTurret("stopX")
        print "Stopping X Movement"

    def right(self,event):
        #turnTurret("right")
        print "Moving right"

    def fireon(self,event):
        #fireTurret() 
        print "Firing"
    def fireoff(self,event):
        #GPIO.output(BLOWER, GPIO.HIGH)
        #GPIO.output(FLYWHEEL, GPIO.HIGH)
        print "Stopping fire sequence"

    def settings(self):
        pass

    def mode(self):    
        autoMode = not autoMode
        print "autoMode is " + autoMode
        
        
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, image = self.photo, anchor = Tkinter.CENTER)
 
        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
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
App(Tkinter.Tk(), "Tkinter and OpenCV")
