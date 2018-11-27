import serial
import sys, pygame
import RPi.GPIO as GPIO
pygame.init()

size = width, height = 320, 240

screen = pygame.display.set_mode(size)

UP = 17
DOWN = 27
LEFT = 22
RIGHT = 23
FLYWHEEL = 24
BLOWER = 25

def GPIO_setup():
	 GPIO.setmode(GPIO.BCM)
	 GPIO.setwarnings(False)
	 GPIO.setup(UP, GPIO.OUT)
	 GPIO.setup(DOWN, GPIO.OUT)
	 GPIO.setup(LEFT, GPIO.OUT)
	 GPIO.setup(RIGHT, GPIO.OUT)
	 GPIO.setup(FLYWHEEL, GPIO.OUT)
	 GPIO.setup(BLOWER,GPIO.OUT)
	 #Initial States
	 GPIO.output(UP, GPIO.HIGH)
	 GPIO.output(DOWN, GPIO.HIGH)
    	 GPIO.output(LEFT, GPIO.HIGH)
    	 GPIO.output(RIGHT, GPIO.HIGH)
   	 GPIO.output(FLYWHEEL, GPIO.HIGH)
   	 GPIO.output(BLOWER, GPIO.HIGH)


GPIO_setup()

while 1:
   # while ser.in_waiting:
#        print(ser.read())

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == 97: #a
                GPIO.output(LEFT, GPIO.LOW)
            elif event.key == 100: # d
                GPIO.output(RIGHT, GPIO.LOW)
            elif event.key == 119: # w
                GPIO.output(UP, GPIO.LOW)
            elif event.key == 115: # s
                GPIO.output(DOWN, GPIO.LOW)
            elif event.key == 113: # q
                GPIO.output(FLYWHEEL, GPIO.LOW)
            elif event.key == 101: #e
                GPIO.output(BLOWER, GPIO.LOW)
		pass
        elif event.type == pygame.KEYUP:
            if event.key == 97: #a
                GPIO.output(LEFT, GPIO.HIGH)
            elif event.key == 100: # d
                GPIO.output(RIGHT, GPIO.HIGH)
            elif event.key == 119: # w
                GPIO.output(UP, GPIO.HIGH)
            elif event.key == 115: # s
                GPIO.output(DOWN, GPIO.HIGH)
	    elif event.key == 113: #q
		GPIO.output(FLYWHEEL, GPIO.HIGH)
	    elif event.key == 101: #e
		GPIO.output(BLOWER, GPIO.HIGH)
		pass
