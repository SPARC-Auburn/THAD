import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import time 
#import RPi.GPIO

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
isRPi = False

#RPi Setup
def GPIO_setup():
    isRPi = True
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
    sleep(2.0)
    GPIO.output(BLOWER, GPIO.LOW)
    sleep(2.0)
    GPIO.output(FLYWHEEL, GPIO.HIGH)
    GPIO.output(BLOWER, GPIO.HIGH)

#GPIO_setup() #UNCOMMENT THIS LINE FOR RUNNING ON RASPBERRY PI

 
class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.window.attributes('-fullscreen', True)
        self.video_source = video_source
        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        self.frame1 = tkinter.Frame(window)
        self.frame1.pack(fill=tkinter.BOTH)
        # Fire Button
        self.btn_fire=tkinter.Button(self.frame1, text="Fire", width=10, height = 2, command=self.fire)
        self.btn_fire.pack(side=tkinter.LEFT, anchor=tkinter.NW, expand=True)
        # Up Button
        self.btn_up=tkinter.Button(self.frame1, text="Up", width=50, height = 2, command=self.up)
        self.btn_up.pack(side = tkinter.LEFT, anchor=tkinter.N, expand=True)
        self.btn_up.bind('<ButtonPress-1>', self.up)
        self.btn_up.bind('<ButtonRelease-1>', self.y_stop)
        # Settings Button
        self.btn_settings=tkinter.Button(self.frame1, text="Settings", width=10, height = 2, command=self.settings)
        self.btn_settings.pack(side = tkinter.LEFT, anchor=tkinter.NE, expand=True)


        self.frame2 = tkinter.Frame(window)
        self.frame2.pack(fill=tkinter.BOTH, expand = True)
        # Left Button
        self.btn_left=tkinter.Button(self.frame2, text="Left", width=10, height = 50, command=self.left)
        self.btn_left.pack(side=tkinter.LEFT, anchor=tkinter.E, expand=True)
        self.btn_left.bind('<ButtonPress-1>', self.left)
        self.btn_left.bind('<ButtonRelease-1>', self.x_stop)
        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.frame2, width = self.vid.width, height = self.vid.height, background='black')
        self.canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH)
        # Right Button
        self.btn_right=tkinter.Button(self.frame2, text="Right", width=10, height=50, command=self.right)
        self.btn_right.pack(side=tkinter.LEFT, anchor=tkinter.W, expand=True)
        self.btn_right.bind('<ButtonPress-1>', self.right)
        self.btn_right.bind('<ButtonRelease-1>', self.x_stop)

        self.frame3 = tkinter.Frame(window)
        self.frame3.pack(fill=tkinter.BOTH)
        # Down Button 
        self.btn_down=tkinter.Button(self.frame3, text="Down", width=50, height = 2)
        self.btn_down.pack(side = tkinter.BOTTOM, anchor=tkinter.S, expand=True)
        self.btn_down.bind('<ButtonPress-1>', self.down)
        self.btn_down.bind('<ButtonRelease-1>', self.y_stop)
        # Mode Button
        self.btn_down=tkinter.Button(self.frame3, text="Auto/Manual", width=50, height = 2, command=self.mode)
        self.btn_down.pack(side = tkinter.BOTTOM, anchor=tkinter.S, expand=True)
        

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()

        self.window.mainloop()

    def down(self,event):
        if isRPi:
            turnTurret("down")

    def y_stop(self,event):
        if isRPi:
            turnTurret("stopY")

    def up(self,event):
        if isRPi:
            turnTurret("up")

    def left(self,event):
        if isRPi:
            turnTurret("left")

    def x_stop(self,event):
        if isRPi:
            turnTurret("stopX")

    def right(self,event):
        if isRPi:
            turnTurret("right")

    def fire(self):
        if isRPi:
            fireTurret() 

    def settings(self):
        pass

    def mode(self):    
        pass
        
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(self.canvas.winfo_width()/2, self.canvas.winfo_height()/2, image = self.photo, anchor = tkinter.CENTER)
 
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
App(tkinter.Tk(), "Tkinter and OpenCV")