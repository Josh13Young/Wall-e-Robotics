import brickpi3
import time
import keyboard
BP = brickpi3.BrickPi3()

motorL = BP.PORT_B
motorR = BP.PORT_C
rotation = 360
def reset():
    BP.offset_motor_encoder(motorR, BP.get_motor_encoder(motorR))
    BP.offset_motor_encoder(motorL, BP.get_motor_encoder(motorL))

def encoder_reached(target_position, motor):
    position = BP.get_motor_encoder(motor)
    return abs(position) >= abs(target_position)
    #return ((abs(position) - abs(target_position)) < 2)
def fwd():
        reset()
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        #BP.set_motor_power(motorR,speed)
        #BP.set_motor_power(motorL,speed)
        BP.set_motor_position(motorR, pos_r + rotation)
        BP.set_motor_position(motorL, pos_l + rotation)
        #while not (encoder_reached(pos_r + rotation, motorR) and encoder_reached(pos_l + rotation, motorL)):
       #        time.sleep(0.1)
def turn():
        reset()
        ang = 420
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        #BP.set_motor_power(motorL, speed)
        #BP.set_motor_power(motorR, -speed)
        BP.set_motor_position(motorR, pos_r - ang)
        BP.set_motor_position(motorL, pos_l + ang)
        #while not (encoder_reached(pos_r - ang, motorR) and encoder_reached(pos_l + ang, motorL)):
        #       time.sleep(0.1)


def star():
        for i in range(5):
            fwd()
            time.sleep(1)
            turn()
            time.sleep(1)

while True:
    if keyboard.is_pressed("s"):
        star()
    elif keyboard.is_pressed("f"):
        fwd()
    elif keyboard.is_pressed("g"):
        turn()
    elif keyboard.is_pressed("x"):
        BP.reset_all()
    time.sleep(0.1)
    
    
