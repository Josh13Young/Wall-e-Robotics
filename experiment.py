import time
import curses

from Bot import PowerControlBot, PositionControlBot, Bot

global_stdscr = None

def curse_print(text):
    global_stdscr.clear()
    global_stdscr.addstr(0, 0, text)
    global_stdscr.refresh()


def task1_control_loop(posBot: "PositionControlBot", letter: str):
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
    elif letter == "y":
        curse_print("Moving in a square")
        posBot.move_square()
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
            inp = global_stdscr.getkey()
            self.control_loop_fn(inp)
            time.sleep(0.1)


def main(stdscr):
    global global_stdscr
    global_stdscr = stdscr

    bot = Bot()
    posControlBot = PowerControlBot(bot, 50)
    
    def control_loop_fn(inp: str):
        task1_control_loop(posControlBot, inp)

    control_proc = ControlProcedure(control_loop_fn)
    control_proc.start_procedure()


if __name__ == "__main__":
    curses.wrapper(main)
