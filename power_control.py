from common import main_wrapper, curse_print, curse_getkey, curses
import time

from Bot import PowerControlBot, Bot


def control_loop(posBot: PowerControlBot, letter: str):
    if letter == "w":
        curse_print("Moving forward")
        posBot.move_forward()
    elif letter == "a":
        curse_print("Turning left")
        posBot.turn_left()
    elif letter == "s":
        curse_print("Moving backward")
        posBot.move_backward()
    elif letter == "d":
        curse_print("Turning right")
        posBot.turn_right()
    elif letter == "x":
        curse_print("Stopping")
        posBot.stop()
    else:
        curse_print(f"Unknown command: {letter}")


class ControlProcedure:
    def __init__(self, control_loop_fn):
        self.control_loop_fn = control_loop_fn
        curses.noecho()

    def start_procedure(self):
        while True:
            inp = curse_getkey()
            self.control_loop_fn(inp)
            time.sleep(0.1)


def main():
    bot = Bot()
    posControlBot = PowerControlBot(bot, 50)

    def control_loop_fn(inp: str):
        control_loop(posControlBot, inp)

    control_proc = ControlProcedure(control_loop_fn)
    control_proc.start_procedure()


if __name__ == "__main__":
    main_wrapper(main)
