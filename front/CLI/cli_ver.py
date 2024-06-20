import sys
sys.path.insert(0, '..')
sys.path.insert(0, '../..')

import curses
import time
import numpy as np

import main_win
import rtl_set_win
import spec_win
import waterfall
import summary

from driver.driver import Driver
from driver.rtl2832u import RTL
from front.CLI.windows.components.options import ActionOptions
from front.CLI.windows.window import Window
from pyfiglet import Figlet


# region [Global vars]

main_screen = curses.initscr()
driver = Driver()

com_port = '0'
central_freq = 0.0  # 1420
sample_rate = 2.048
tuner_gain = 'auto'
sample_count = '512'

# endregion

# region [Windows]

def main_window():
    main_win.generate()


def rtl_setup():
    rtl_set_win.generate()


def spectrum_window():
    spec_win.generate()


def waterfall_window():
    waterfall.generate()

def summary_window():
    summary.generate()

# endregion


try:
    if __name__ == "__main__":
        main_window()
except KeyboardInterrupt:
    curses.endwin()
