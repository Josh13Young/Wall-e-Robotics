import math
import time

import brickpi3 #import BrickPi.py file to use BrickPi operations

import curses   # import curses for text processing

# set up curses interface

stdscr = curses.initscr()
curses.noecho()

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
motorR = BP.PORT_B # right motor
motorL = BP.PORT_C # left motor
speed = 360   # range is -255 to 255, make lower if bot it too fast
x, y, theta = 0.0, 0.0, 0.0

BP.set_motor_limits(motorR, 50)
BP.set_motor_limits(motorL, 50)

#Move Forward

def fwd():
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        #BP.set_motor_power(motorR,speed)
        #BP.set_motor_power(motorL,speed)
        BP.set_motor_position(motorR, pos_r + speed)
        BP.set_motor_position(motorL, pos_l + speed)
def left():
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        #BP.set_motor_power(motorL, speed)
        #BP.set_motor_power(motorR, -speed)
        BP.set_motor_position(motorR, pos_r - 270)
        BP.set_motor_position(motorL, pos_l + 270)
        while not (encoder_reached(pos_r - 270, motorR) and encoder_reached(pos_l + 270, motorL)):
               time.sleep(0.1)
#Move Right
def right():
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        BP.set_motor_position(motorR, pos_r + 270)
        BP.set_motor_position(motorL, pos_l - 270)

#Stop
def stop():
        BP.set_motor_power(motorR, 0)
        BP.set_motor_power(motorL, 0)


def navigateToWaypoint(wx, wy):
    meter = (833 / 4) * 10
    rotate = 1080
    global x
    global y
    global theta
    x_new, y_new = wx - x, wy - y
    angle = math.degrees(math.atan2(y_new, x_new)) - theta
    dist = math.sqrt(x_new**2 + y_new**2)
    pos_r = BP.get_motor_encoder(motorR)
    pos_l = BP.get_motor_encoder(motorL)
#    if (angle > 180):
#        angle -= 180
#    elif (angle < 180):
#        angle += 180
    motorTurnAmount = rotate * (angle / 360)
    motorDriveAmount = meter * dist

    BP.set_motor_position(motorR, pos_r - motorTurnAmount)
    BP.set_motor_position(motorL, pos_l + motorTurnAmount)
    time.sleep(2)
    pos_r = BP.get_motor_encoder(motorR)
    pos_l = BP.get_motor_encoder(motorL)
    BP.set_motor_position(motorR, pos_r + motorDriveAmount)
    BP.set_motor_position(motorL, pos_l + motorDriveAmount)
    x, y = wx, wy
    a = theta + angle
#    if a > 180:
#        a -= 180
#    elif a < 180:
#        a += 180
    theta = a
    print(x_new)
    print(y_new)
    print(theta)
    time.sleep(4)


try:
        while True:
                inp_x = stdscr.getkey() 
                inp_y = stdscr.getkey() 
                navigateToWaypoint(float(inp_x), float(inp_y))

                time.sleep(0.01)
except KeyboardInterrupt:
        BP.reset_all()

