import curses
import time

stdscr: curses.window


def main_wrapper(main):
    def wrap(local_stdscr):
        global stdscr
        stdscr = local_stdscr
        main()

    curses.wrapper(wrap)


def curse_print(text):
    stdscr.clear()
    stdscr.addstr(0, 0, text)
    stdscr.refresh()


def curse_getkey():
    return stdscr.getkey()


def curse_noecho():
    curses.noecho()


class ControlProcedure:
    def __init__(self, control_loop_fn):
        self.control_loop_fn = control_loop_fn
        curse_noecho()

    def start_procedure(self):
        while True:
            inp = curse_getkey()
            self.control_loop_fn(inp)
            time.sleep(0.1)
