from common.common import frange3
from front.windows.windows.main_win import MainMenu

import curses


# region [Global vars]

main_screen = curses.initscr()
main_window = MainMenu(None, main_screen)

# endregion


# region [Windows]

def kill(message):
    curses.endwin()
    exit(message)


def main():
    try:
        main_window.generate()
    except KeyboardInterrupt:
        kill('exit')

# endregion


try:
    if __name__ == "__main__":
        curses.start_color()
        curses.use_default_colors()
        main()
except KeyboardInterrupt:
    curses.endwin()
