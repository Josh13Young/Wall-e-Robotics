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
#from star import encoder_reached
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
#Move Forward

def fwd():
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        #BP.set_motor_power(motorR,speed)
        #BP.set_motor_power(motorL,speed)
        BP.set_motor_position(motorR, pos_r + speed)
        BP.set_motor_position(motorL, pos_l + speed)
def fwdS():
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        #BP.set_motor_power(motorR,speed)
        #BP.set_motor_power(motorL,speed)
        BP.set_motor_position(motorR, pos_r + 800)
        BP.set_motor_position(motorL, pos_l + 800)
  #      while not (encoder_reached(pos_r + 800, motorR) and encoder_reached(pos_l + 800, motorL)):
   #            time.sleep(0.1)
#Move Left
def left():
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        #BP.set_motor_power(motorL, speed)
        #BP.set_motor_power(motorR, -speed)
        BP.set_motor_position(motorR, pos_r - 260)
        BP.set_motor_position(motorL, pos_l + 260)
#        while not (encoder_reached(pos_r - 260, motorR) and encoder_reached(pos_l + 260, motorL)):
 #              time.sleep(0.1)

#Move Right
def right():
        #BP.set_motor_power(motorL, -speed)
        #BP.set_motor_power(motorR, speed)
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        BP.set_motor_position(motorR, pos_r + 250)
        BP.set_motor_position(motorL, pos_l - 250)

#Move backward
def back():
        pos_l = BP.get_motor_encoder(motorL)
        pos_r = BP.get_motor_encoder(motorR)
        #BP.set_motor_power(motorR, -speed)
        #BP.set_motor_power(motorL, -speed)
        BP.set_motor_position(motorR, pos_r - speed)
        BP.set_motor_position(motorL, pos_l - speed)

#Stop
def stop():
        BP.set_motor_power(motorR, 0)
        BP.set_motor_power(motorL, 0)

def square():
        for i in range(4):
                fwdS()
                time.sleep(1.5)
                left()
                time.sleep(1)

while True:
    inp = stdscr.getkey() #Take input from the terminal
    #Move the bot
    if inp == 'w':
        fwd()
        print("fwd\n")
    elif inp=='a' :
        left()
        print("left\n")
    elif inp=='d':
        right()
        print("right\n")
    elif inp=='s':
        back()
        print("back\n")

    elif inp=='t':
        fwdS()
        print("40cm\n")
    elif inp =='y':
        square()
        print("square\n")
    elif inp=='x':
         stop()
    time.sleep(.01)         # sleep for 10 ms


