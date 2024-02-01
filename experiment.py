import time
import curses

from Bot import PositionControlBot, Bot


def task1_control_loop(posBot: "PositionControlBot", letter: str):
    if letter == "w":
        print("Moving forward")
        posBot.move_forward()
    elif letter == "a":
        print("Turning left")
        posBot.turn_left()
    elif letter == "s":
        print("Moving backward")
        posBot.move_backward()
    elif letter == "d":
        print("Turning right")
        posBot.turn_right()
    elif letter == "y":
        print("Moving in a square")
        posBot.move_square()
    elif letter == "x":
        print("Stopping")
        posBot.stop()
    else:
        print(f"Unknown command: {letter}")


class ControlProcedure:
    def __init__(self, control_loop_fn):
        self.stdscr = curses.initscr()
        self.control_loop_fn = control_loop_fn
        curses.noecho()

    def start_procedure(self):
        while True:
            inp = self.stdscr.getkey()
            self.control_loop_fn(inp)
            time.sleep(0.1)


if __name__ == "__main__":
    bot = Bot()
    posControlBot = PositionControlBot(bot)

    def control_loop_fn(inp: str):
        task1_control_loop(posControlBot, inp)

    control_proc = ControlProcedure(control_loop_fn)
    control_proc.start_procedure()
