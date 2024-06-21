import sys

sys.path.insert(0, '..')
sys.path.insert(0, '../..')

import curses

import main_win
import rtl_set_win
import spec_win
import waterfall
import summary
import  xy_set_win

from driver.driver import Driver


# region [Global vars]

main_screen = curses.initscr()
rtl_driver = Driver()

rtl_com_port = '0'
central_freq = 0.0  # 1420
sample_rate = 2.048
tuner_gain = 'auto'
sample_count = '512'

stm32_driver = Driver()

rotor_com_port = '0'
rotor_power = 0
rotor_radius = 0
antenna_radius = 0

# endregion


# region [Windows]

def kill(message):
    curses.endwin()
    exit(message)


def main_window():
    try:
        main_win.generate()
    except KeyboardInterrupt:
        print('exit')


def rtl_setup():
    try:
        rtl_set_win.generate()
    except Exception as e:
        kill('Something go wrong')


def xy_setup():
    try:
        xy_set_win.generate()
    except Exception as e:
        kill('Something go wrong')


def spectrum_window():
    try:
        spec_win.generate()
    except Exception as e:
        kill('Something go wrong\nMaybe you forgot link RTL-SDR?')


def waterfall_window():
    try:
        waterfall.generate()
    except Exception as e:
        kill('Something go wrong\nMaybe you forgot link RTL-SDR?')


def summary_window():
    try:
        summary.generate()
    except Exception as e:
        kill('Something go wrong')

# endregion


try:
    if __name__ == "__main__":
        main_window()
except KeyboardInterrupt:
    curses.endwin()
