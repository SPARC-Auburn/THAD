import serial
import sys, pygame
pygame.init()

size = width, height = 320, 240
ser = serial.Serial("COM3")

screen = pygame.display.set_mode(size)

while 1:
    while ser.in_waiting:
        print(ser.read())

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == 97: #a
                ser.write('a')
            elif event.key == 100: # d
                ser.write('d')
            elif event.key == 119: # w
                ser.write('w')
            elif event.key == 115: # s
                ser.write('s')   
				
            elif event.key == 113: # q
                ser.write('q')
            elif event.key == 101: #e
                #ser.write(bytes([3,64]))
		pass
        elif event.type == pygame.KEYUP:
            if event.key == 97: #a
                ser.write('f')
            elif event.key == 100: # d
                ser.write('h')
            elif event.key == 119: # w
                ser.write('t')
            elif event.key == 115: # s
                ser.write('g') 