import time
import curses

from Bot import PositionControlBot, Bot


def task1_control_loop(posBot: "PositionControlBot", letter: str):
    match letter:
        case "w":
            print("Moving forward")
            posBot.move_forward()
        case "a":
            print("Turning left")
            posBot.turn_left()
        case "s":
            print("Moving backward")
            posBot.move_backward()
        case "d":
            print("Turning right")
            posBot.turn_right()
        case "y":
            print("Moving in a square")
            posBot.move_square()
        case "x":
            print("Stopping")
            posBot.stop()
        case _:
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
