"""
The robot will use its ultrasonic sensor to maintain a set distance
  (TARGET_DIST) from the wall on its side
"""

from collections import deque

from common import main_wrapper, curse_print
from bot_control.Bot import Bot
from bot_control.VelocityControl import VelocityControlBot
import time

TARGET_DIST: int = 30 # in cm
PROPORTIONAL_CONSTANT = 5
MAX_SPEED = 300
TEMPORAL_FILTERING_WINDOW = 5 # num samples
BOT_SPEED = 200

def median_value(q: deque[int]) -> int:
    if len(q) == 0:
      return 0
    return sorted(q)[len(q) // 2]

def control_loop(bot: Bot, velBot: VelocityControlBot):
    # short sleep to allow the motors to accelerate a bit before the next command
    short_sleep = lambda: time.sleep(0.3)

    # very short sleep to add a short delay between motor commands
    very_short_sleep = lambda: time.sleep(0.05)
    short_sleep()
    
    velBot.go_forwards(BOT_SPEED)
    
    previous_readings = deque()

    while True:
        very_short_sleep()
        raw_reading = bot.get_ultrasonic_sensor_value()
        reading = raw_reading
        
        if len(previous_readings) != 0:
          median = median_value(previous_readings)
          if abs(median - raw_reading) > 10:
            reading = median
          
        previous_readings.append(raw_reading)
        if len(previous_readings) > TEMPORAL_FILTERING_WINDOW:
          previous_readings.popleft()
          
        error_term = PROPORTIONAL_CONSTANT * (reading - TARGET_DIST) // 2
        left_speed = BOT_SPEED - error_term
        right_speed = BOT_SPEED + error_term
        
        bot.set_left_velocity_dps(left_speed)
        bot.set_right_velocity_dps(right_speed)
            

def main():
    bot = Bot()
    velControlBot = VelocityControlBot(bot, BOT_SPEED)
    
    control_loop(bot, velControlBot)


if __name__ == "__main__":
    main_wrapper(main)
