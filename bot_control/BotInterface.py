
from collections import namedtuple
from abc import ABC, abstractmethod
import time

MotorStatus = namedtuple(
    "MotorStatus", ["status_flag", "power_percent", "encoder_pos", "velocity_dps"]
)

class BotInterface(ABC):
    @abstractmethod
    def reset_encoders(self):
        return

    @abstractmethod
    def reset_motor_power(self):
        return

    @abstractmethod
    def set_motor_limits(self, motor_limit: int):
        return

    @abstractmethod
    def set_left_power(self, power: int):
        return

    @abstractmethod
    def set_right_power(self, power: int):
        return

    @abstractmethod
    def set_left_position(self, position: int):
        return

    @abstractmethod
    def set_right_position(self, position: int):
        return

    @abstractmethod
    def get_right_position(self) -> int:
        return

    @abstractmethod
    def get_left_position(self) -> int:
        return

    @abstractmethod
    def get_left_status(self) -> MotorStatus:
        return

    @abstractmethod
    def get_right_status(self) -> MotorStatus:
        return

    @abstractmethod
    def set_left_velocity_dps(self, velocity_dps: int):
        return

    @abstractmethod
    def set_right_velocity_dps(self, velocity_dps: int):
        return

    @abstractmethod
    def get_left_velocity_dps(self) -> int:
        return

    @abstractmethod
    def get_right_velocity_dps(self) -> int:
        return

    @abstractmethod
    def get_left_touch_sensor_value(self) -> int:
        return

    @abstractmethod
    def get_right_touch_sensor_value(self) -> int:
        return

    @abstractmethod
    def get_ultrasonic_sensor_value(self) -> int:
        return
      
class ControlBot(ABC):
    def __init__(self, bot: BotInterface, motor_limit: int = 50):
        self.bot = bot
        self.bot.set_motor_limits(motor_limit)

    def stop(self):
        self.bot.reset_motor_power()

    def wait_for_movement_completion(self):
        dps_l = self.bot.get_left_velocity_dps()
        dps_r = self.bot.get_right_velocity_dps()
        start_time = time.time()
        while dps_l != 0 or dps_r != 0: # assume up to 0.5s will be taken to do movements
            if start_time - time.time() >= 0.5:
                print("     -> we've slept for over 0.5s waiting for the robot to stop moving")
                return
            
            time.sleep(0.1)
            dps_l = self.bot.get_left_velocity_dps()
            dps_r = self.bot.get_right_velocity_dps()
