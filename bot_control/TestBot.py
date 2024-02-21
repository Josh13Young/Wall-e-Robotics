from bot_control.BotInterface import BotInterface, MotorStatus
import time
import math
import random

class TestBot(BotInterface):
    def __init__(self):
        self.offset_left = 0
        self.offset_right = 0
        
        self.power_left = 0
        self.power_right = 0
        
        self.velocity_left = 0
        self.velocity_right = 0
        
        self.power_limit = 0

    def reset_encoders(self):
        self.offset_left = 0
        self.offset_right = 0

    def reset_motor_power(self):
        self.power_left = 0
        self.power_right = 0

    def set_motor_limits(self, motor_limit: int):
        self.power_limit = motor_limit

    def set_left_power(self, power: int):
        self.power_left = power

    def set_right_power(self, power: int):
        self.power_right = power

    def set_left_position(self, position: int):
        self.offset_left = position

    def set_right_position(self, position: int):
        self.offset_right = 0

    def get_right_position(self) -> int:
        return self.offset_right

    def get_left_position(self) -> int:
        return self.offset_left

    def get_left_status(self) -> MotorStatus:
        return MotorStatus(0, 0, self.offset_left, self.velocity_left)

    def get_right_status(self) -> MotorStatus:
        return MotorStatus(0, 0, self.offset_right, self.velocity_right)

    def set_left_velocity_dps(self, velocity_dps: int):
        self.velocity_left = velocity_dps

    def set_right_velocity_dps(self, velocity_dps: int):
        self.velocity_right = velocity_dps

    def get_left_velocity_dps(self) -> int:
        return self.velocity_left

    def get_right_velocity_dps(self) -> int:
        return self.velocity_right

    def get_left_touch_sensor_value(self) -> int:
        return random.randint(0, 1)

    def get_right_touch_sensor_value(self) -> int:
        return random.randint(0, 1)

    def get_ultrasonic_sensor_value(self) -> int:
        return int(math.cos(time.time()/10)**2 * 235 + 20)
