# Program Name: simplebot_simple.py

# ================================

# This code is for moving the simplebot

# Author     Date      Comments
# Karan      04/11/13  Initial Authoring
#
# These files have been made available online through a Creative
# Commons Attribution-ShareAlike 3.0  license.
# (http://creativecommons.org/licenses/by-sa/3.0/)

# Revised by T. Cooper 12/18

# --- program updated for Python 3

# --- curses interface added for consistent input mang.

#Commands:

#       w-Move forward

#       a-Move left

#       d-Move right

#       s-Move back

#       x-Stop

# we add these libraries to give us the ability to use sleep func

# use Brick Pi 3 stuff and the curses interface (it makes input easier and consistent)

import time

import brickpi3 #import BrickPi.py file to use BrickPi operations

import curses   # import curses for text processing

import keyboard # import keyboard for more responsive polling (i think requires sudo)

# set up curses interface

stdscr = curses.initscr()
curses.noecho()

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.
motorR = BP.PORT_B # right motor
motorL = BP.PORT_C # left motor
speed = 50# range is -255 to 255, make lower if bot it too fast
#Move Forward

def fwd():
        BP.set_motor_power(motorR,speed)
        
        BP.set_motor_power(motorL,speed)
 #       time.sleep(0.1)
        

 #       BP.set_motor_power(motorR,0)

#        BP.set_motor_power(motorL,0)
#Move Left
def left():
        BP.set_motor_power(motorL, speed)
        BP.set_motor_power(motorR, -speed)

#Move Right
def right():
        BP.set_motor_power(motorL, -speed)
        BP.set_motor_power(motorR, speed)

#Move backward
def back():
        BP.set_motor_power(motorR, -speed)
        BP.set_motor_power(motorL, -speed)
#Move diagonal Forward-Right
def diag_FR():
        BP.set_motor_power(motorR, speed/2)
        BP.set_motor_power(motorL, speed)
#Stop
def stop():
        BP.set_motor_power(motorR, 0)
        BP.set_motor_power(motorL, 0)

while True:
        #Move the bot
        if keyboard.is_pressed("w"):
            while keyboard.is_pressed("w"):
                fwd()
                print("fwd")
            stop()
        elif keyboard.is_pressed("e"):
            while keyboard.is_pressed("e"):
                diag_FR()
                print("diag-forw-right")
            stop()
        elif keyboard.is_pressed("a") :
            while keyboard.is_pressed("a"):
                left()
                print("left")
            stop()

        elif keyboard.is_pressed("d"):
            while keyboard.is_pressed("d"):
                right()
                print("right")
            stop()

        elif keyboard.is_pressed("s"):
            while keyboard.is_pressed("s"):
                back()
                print("back")
            stop()

        elif keyboard.is_pressed("x"):
                stop()

        time.sleep(.01)         # sleep for 10 ms
