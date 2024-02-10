import curses

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
