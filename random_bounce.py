from common import main_wrapper, curse_print, ControlProcedure
from bot_control.Bot import Bot
from bot_control.PositionControl import PositionControlBot
from bot_control.VelocityControl import VelocityControlBot
import time


def control_loop(posBot: PositionControlBot, velBot: VelocityControlBot, letter: str):
    if letter == "w":
        velBot.stop()
        time.sleep(0.1)
        curse_print("Moving forward (using velocity control)")
        velBot.go_forwards()
    elif letter == "a":
        velBot.stop()
        time.sleep(0.1)
        curse_print("Turning left (using position control)")
        posBot.turn_left()
    elif letter == "s":
        velBot.stop()
        time.sleep(0.1)
        curse_print("Moving backward (using velocity control)")
        velBot.go_backwards()
    elif letter == "d":
        velBot.stop()
        time.sleep(0.1)
        curse_print("Turning right (using position control)")
        posBot.turn_right()
    elif letter == "x":
        curse_print("Stopping")
        posBot.stop()
    else:
        curse_print(f"Unknown command: {letter}")


def main():
    bot = Bot()
    posControlBot = PositionControlBot(bot, 50)
    velControlBot = VelocityControlBot(bot, 120)

    def control_loop_fn(inp: str):
        control_loop(posControlBot, velControlBot, inp)

    control_proc = ControlProcedure(control_loop_fn)
    control_proc.start_procedure()


if __name__ == "__main__":
    main_wrapper(main)
