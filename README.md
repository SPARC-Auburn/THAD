# THAD
## The Helpful Automated Defender  

## Project Purpose

THAD was previously a senior design project, and was given to SPARC in a state that did not operate. The goal of the project was to return it to working order and enable it with computer vision to be able to shoot the user's hand. This will facilitate a great project for demos and shows.

## Project Overview

The turret itself is mounted on a large, 2 axis motor, using a Nerf gun and seperate blower as its firing mechanism. The turret is controlled by a 5V 8-relay module to an Arduino. The arduino responds to serial commands. These commands are sent from various sources, and all that is required are (W,A,S,D,Q) characters to be sent over serial to operate. (These are Up, Left, Down, Right, and Fire respectively)

## Setup and Use

### Manual

To run the turret manually via keyboard: 
1. Upload the .ino file located in the Manual folder to the Arduino. 
1. The Arduino pinout should be as follows:
  * DIO2 - Fire(Fan)
  * DIO3 - Flywheel(Trigger)
  * DIO4 - Up
  * DIO5 - Down
  * DIO6 - CW(Right)
  * DIO7 - CCW(Left)
  * Note: The Fan requires 27VDC
3. With the a PC still plugged in to the Arduino, run the keyboardserial.py program
  * You may have to change the port in the .py code. Simply change "COM3" to the port the Arduino is plugged into.
4. With the PyGame window active, use the keys W,A,S,D and Q to control the turret.  

### OpenCV(Computer Vision)
