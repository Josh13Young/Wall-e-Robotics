try:
  import brickpi3
except:
  pass

import random

from bot_control.BotInterface import BotInterface, MotorStatus
import time
import math


class Bot(BotInterface):
    BP: brickpi3.BrickPi3 = None

    @staticmethod
    def _reset_bp():
        if Bot.BP:
            Bot.BP.reset_all()

    def __init__(self):
        if not Bot.BP:
            self.BP = brickpi3.BrickPi3()
            Bot.BP = self.BP
        else:
            self.BP = Bot.BP

        Bot._reset_bp()  # ensure everything is unconfigured

        self.motorR = self.BP.PORT_C
        self.motorL = self.BP.PORT_B

        self.touchSensorR = self.BP.PORT_1
        self.touchSensorL = self.BP.PORT_4

        self.ultrasonicSensor = self.BP.PORT_3

        self.BP.set_sensor_type(self.touchSensorR, self.BP.SENSOR_TYPE.TOUCH)
        self.BP.set_sensor_type(self.touchSensorL, self.BP.SENSOR_TYPE.TOUCH)
        self.BP.set_sensor_type(
            self.ultrasonicSensor, self.BP.SENSOR_TYPE.NXT_ULTRASONIC
        )

        self.reset_encoders()
        self.reset_motor_power()

    def reset_encoders(self):
        lpos = self.get_left_position()
        rpos = self.get_right_position()

        self.BP.offset_motor_encoder(self.motorL, lpos)
        self.BP.offset_motor_encoder(self.motorR, rpos)

    def reset_motor_power(self):
        self.set_left_power(0)
        self.set_right_power(0)

    def set_motor_limits(self, motor_limit: int):
        self.BP.set_motor_limits(self.motorL, motor_limit)
        self.BP.set_motor_limits(self.motorR, motor_limit)

    def set_left_power(self, power: int):
        self.BP.set_motor_power(self.motorL, power)

    def set_right_power(self, power: int):
        self.BP.set_motor_power(self.motorR, power)

    def set_left_position(self, position: int):
        self.BP.set_motor_position(self.motorL, position)

    def set_right_position(self, position: int):
        self.BP.set_motor_position(self.motorR, position)

    def get_right_position(self) -> int:
        return self.BP.get_motor_encoder(self.motorR)

    def get_left_position(self) -> int:
        return self.BP.get_motor_encoder(self.motorL)

    def get_left_status(self) -> MotorStatus:
        return MotorStatus(*self.BP.get_motor_status(self.motorL))

    def get_right_status(self) -> MotorStatus:
        return MotorStatus(*self.BP.get_motor_status(self.motorR))

    def set_left_velocity_dps(self, velocity_dps: int):
        self.BP.set_motor_dps(self.motorL, velocity_dps)

    def set_right_velocity_dps(self, velocity_dps: int):
        self.BP.set_motor_dps(self.motorR, velocity_dps)

    def get_left_velocity_dps(self) -> int:
        return self.get_left_status().velocity_dps

    def get_right_velocity_dps(self) -> int:
        return self.get_right_status().velocity_dps

    def get_left_touch_sensor_value(self) -> int:
        return self.BP.get_sensor(self.touchSensorL)

    def get_right_touch_sensor_value(self) -> int:
        return self.BP.get_sensor(self.touchSensorR)

    def get_ultrasonic_sensor_value(self) -> int:
        """Returns distance of obstacle in front of sensor (up to 255cm away)"""
        value = None
        mark_time = time.time()
        while value == None:
            try:
                reading = self.BP.get_sensor(self.BP.PORT_3)
                value = reading
            except brickpi3.SensorError:
                if time.time() - mark_time > 0.5: # 0.2s have passed
                    mark_time = time.time()
                    print("0.2s have passed while trying to get a non garbage sensor reading")
            time.sleep(0.02)
        return value
