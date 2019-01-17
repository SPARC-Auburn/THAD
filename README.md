# THAD
## The Helpful Automated Defender  

<img src="CV Control/IMG_6561.JPG" height = "360" width = "640" alt="THAD"></img>

## Project Purpose

THAD was previously a senior design project, and was given to SPARC in a state that did not operate. The goal of the project was to return it to working order and enable it with computer vision to be able to shoot the user's hand. This will facilitate a great project for demos and shows.

## Project Overview (NEEDS UPDATE)

The turret itself is mounted on a large, 2 axis motor, using a Nerf gun and seperate blower as its firing mechanism. The turret is controlled by a 5V 8-relay module to an Arduino. The arduino responds to serial commands. These commands are sent from various sources, and all that is required are (W,A,S,D,Q) characters to be sent over serial to operate. (These are Up, Left, Down, Right, and Fire respectively)

Using these serial commands, automatic control is also possible through OpenCV. The current version uses face recognition to determine targets, then crops a portion of the screen where the right hand might be relative to that face. Using the cropped image, it attempts to detect a right hand in a clenched fist. Future versions will ideally be able to handle multiple targets and a new haar cascade for an open hand.

<img src="CV Control/Hand Targeting.jpg" height = "300" width = "399" alt="Face Recognition"></img>

## Setup and Use

### Manual (NEEDS UPDATE)

<img src="CV Control/IMG_6565.JPG" height= "300" width = "399" alt="Control Box"></img>

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

### OpenCV(Computer Vision) (NEEDS UPDATE)

To run the turret via OpenCV:
1. Ensure Python 2.7 and OpenCV are compiled and usable natively from your OS Path.
1. Follow Step 2 from above to properly wire the turret.
1. Plug your computer into the webcam and Arduino located on THAD
1. Run the main.py program- it will currently only fire at a person's hand, and does not work well with multiple faces detected in the frame.
1. Get ready!

## Future Improvements

## References

1. "Hand-raising gesture detection with Lienhart-Maydt method in videoconference and distance learning" http://conteudo.icmc.usp.br/pessoas/moacir/papers/NazarePonti_CIARP2013.pdf
