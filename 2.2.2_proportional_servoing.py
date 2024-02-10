"""
The robot will use its ultrasonic sensor to maintain a set distance
  (TARGET_DIST) from whatever is in front of it
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

def median_value(q: deque):
    if len(q) == 0:
      return 0
    return sorted(q)[len(q) // 2]

def control_loop(bot: Bot, velBot: VelocityControlBot):
    # short sleep to allow the motors to accelerate a bit before the next command
    short_sleep = lambda: time.sleep(0.3)

    # very short sleep to add a short delay between motor commands
    very_short_sleep = lambda: time.sleep(0.05)
    short_sleep()
    
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
        
        if reading < TARGET_DIST:
            error = TARGET_DIST - reading
            proportional_speed = min(error * PROPORTIONAL_CONSTANT, MAX_SPEED)
            velBot.go_backwards(proportional_speed)
            curse_print(f"Going backwards at speed: {proportional_speed}")
        elif reading > TARGET_DIST:
            error = reading - TARGET_DIST
            proportional_speed = min(error * PROPORTIONAL_CONSTANT, MAX_SPEED)
            velBot.go_forwards(proportional_speed)
            curse_print(f"Going forwards at speed: {proportional_speed}")
            


def main():
    bot = Bot()
    velControlBot = VelocityControlBot(bot, 200)
    
    control_loop(bot, velControlBot)


if __name__ == "__main__":
    main_wrapper(main)
