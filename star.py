import brickpi3
import time
BP = brickpi3.BrickPi3()

motorL = BP.PORT_B
motorR = BP.PORT_C
rotation = 360
# BP.offset_motor_encoder(motorR, BP.get_motor_encoder(motorR)):

def encoder_reached(target_position, motor):
    position = BP.get_motor_encoder(motor)
    return abs(position) >= abs(target_position)
    # return ((abs(left_position) - abs(target_position)) < 2) and ((abs(right_position) - abs(target_position)) < 2)
def fwd():
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        #BP.set_motor_power(motorR,speed)
        #BP.set_motor_power(motorL,speed)
        BP.set_motor_position(motorR, pos_r + rotation)
        BP.set_motor_position(motorL, pos_l + rotation)
        while not (encoder_reached(pos_r + rotation, motorR) and encoder_reached(pos_l + rotation, motorL)):
               time.sleep(0.1)
def turn():
        pos_r = BP.get_motor_encoder(motorR)
        pos_l = BP.get_motor_encoder(motorL)
        #BP.set_motor_power(motorL, speed)
        #BP.set_motor_power(motorR, -speed)
        BP.set_motor_position(motorR, pos_r - 144)
        BP.set_motor_position(motorL, pos_l + 144)
        while not (encoder_reached(pos_r - 144, motorR) and encoder_reached(pos_l + 144, motorL)):
               time.sleep(0.1)


def star():
        for i in range(5):
            fwd()
            turn()
try:
       star()
       BP.reset_all()




except KeyboardInterrupt:
        BP.reset_all()
    
