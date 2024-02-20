import math
import time

import brickpi3 #import BrickPi.py file to use BrickPi operations

import curses   # import curses for text processing

# set up curses interface

stdscr = curses.initscr()
curses.noecho()

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
motorR = BP.PORT_C # right motor
motorL = BP.PORT_B # left motor
speed = 360   # range is -255 to 255, make lower if bot it too fast
x, y, theta = 0.0, 0.0, 0.0

BP.set_motor_limits(motorR, 50)
BP.set_motor_limits(motorL, 50)

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

    motorDriveAmount = meter * dist
    print("angle: " + str(angle))
    if angle < -180:
        angle += 360
    elif angle > 180:
        angle -= 360
    motorTurnAmount = rotate * (angle / 360)
    BP.set_motor_position(motorR, pos_r + motorTurnAmount)
    BP.set_motor_position(motorL, pos_l - motorTurnAmount)
    time.sleep(2)
    pos_r = BP.get_motor_encoder(motorR)
    pos_l = BP.get_motor_encoder(motorL)
    BP.set_motor_position(motorR, pos_r + motorDriveAmount)
    BP.set_motor_position(motorL, pos_l + motorDriveAmount)
    x, y = wx, wy
    theta += angle
    time.sleep(4)


try:
    while True:
            #inp_x = stdscr.getkey() 
            #inp_y = stdscr.getkey()
            stdscr.clear()
            stdscr.addstr(0, 0, "Waypoint coordinate in format x,y")
            stdscr.refresh()
            curses.echo()
            inp = stdscr.getstr(1,0).decode(encoding='utf-8')
            curses.noecho()
            x_str, y_str = map(str.strip, inp.split(','))
            inp_x = float(x_str)
            inp_y = float(y_str)         
            print(f"moving to ({inp_x}, {inp_y})")  
            navigateToWaypoint(inp_x, inp_y)
            time.sleep(0.01)
except KeyboardInterrupt:
    stop()
    BP.reset_all()
        

