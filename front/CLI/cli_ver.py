import curses
import time

import numpy as np

from driver.driver import Driver
from driver.rtl2832u import RTL
from front.CLI.windows.components.options import ActionOptions
from front.CLI.windows.window import Window
from pyfiglet import Figlet

main_screen = curses.initscr()
driver = Driver()


# region [Main]

def main_window_generator():
    options = [
        "0) RTL-SDR setup", "1) X&Y setup",
        "2) Real-time spectrum", "3) Real-time waterfall",
        "4) Real-time movement", "5) Summary"
    ]

    descriptions = [
        "This window will give interface for setting RTL-SDR COM-port. In different OS COM-ports named differend. You "
        "should do this as first step.",
        "XY setup needed when you have navigation system of two or more motors. There you can choose COM-port, "
        "power and other stuff.",
        "Spectrum analyzer window show spectrum in real time. RTL-SDR send data by serial port to Cordell RSA, "
        "then Cordell RSA draw graphs of spectrum.",
        "Waterfall window is a second part of spectrum window. Every second this window draws line of spectrum, "
        "store, and move it down. With this window you can find blinking signal.",
        "XY movement window for working with your navigation system. Don`t forget check XY setup window.",
        "Summary window includes data about authors and simple guide how to create your own radio-telescope"
    ]

    actions = [lambda: rtl_setup_window(), None, lambda: spectrum_window(), lambda: waterfall_window(), None, None]

    window = Window([ActionOptions(1, 2, options, descriptions, actions, main_screen)], main_screen)
    window.draw()

    window.take_control()


# endregion

# region [RTL setup]

com_port = '0'
central_freq = 'none'  # 1420
sample_rate = '2.048'
tuner_gain = 'auto'
sample_count = '512'


def rtl_setup_window():
    global com_port, central_freq, sample_count, sample_rate, tuner_gain

    options = [
        f"0) COM-port <{com_port}>", f"1) Center frequency <{central_freq} mHz>", f"2) Sample rate <{sample_rate} mHz>",
        f"3) Tuner gain mode <{tuner_gain}>", f"4) Sample count <{sample_count}>", "5) Exit"
    ]

    descriptions = [
        "The COM port used to communicate with the device. Specify the port number to which the device is connected."
        f"\nEnabled devices: \n{' '.join(str(element) for element in RTL.get_serials())}",
        "The center frequency that the receiver is tuned to. Specify the value in MHz.",
        "The sampling rate for capturing signals. Specify the value in MHz.",
        "The tuner gain mode. Choose the mode that controls the gain level for signal reception.",
        "Count of samples",
        "<EXIT>"
    ]

    # region [RTL win handlers]

    def com(body: ActionOptions, data):
        global com_port, driver

        index = int(data)
        body.options[0] = f"0) COM-port <index: {index} ({RTL.get_serials()[index]})>"

        driver = RTL(RTL.get_serials()[index])
        driver.set_sample_count(512)
        driver.set_gain('auto')
        driver.set_sample_rate(2.048e6)

        main_screen.refresh()

    def cfreq(body: ActionOptions, data):
        global central_freq, driver
        central_freq = int(data)
        body.options[1] = f"1) Center frequency <{central_freq} mHz>"

        driver.set_central_freq(central_freq * 10e6)

        main_screen.refresh()

    def srate(body: ActionOptions, data):
        global sample_rate, driver
        sample_rate = int(data)
        body.options[2] = f"2) Sample rate <{sample_rate} mHz>"

        driver.set_sample_rate(sample_rate * 10e6)

        main_screen.refresh()

    def tuner(body: ActionOptions, data):
        global tuner_gain, driver
        tuner_gain = data
        body.options[3] = f"3) Tuner gain mode <{tuner_gain}>"

        driver.set_gain(tuner_gain)

        main_screen.refresh()

    def scount(body: ActionOptions, data):
        global sample_count, driver
        sample_count = int(data)
        body.options[4] = f"4) Sample count <{sample_count}>"

        driver.set_sample_count(sample_count)

        main_screen.refresh()

    def wexit(body: ActionOptions):
        body.parent.untie()
        main_window_generator()

    # endregion

    actions = [com, cfreq, srate, tuner, scount, wexit]

    window = Window([ActionOptions(1, 2, options, descriptions, actions, main_screen)], main_screen)
    window.draw()

    window.take_control()


# endregion

# region [Spectrum]

spectrum_break_loop = True


def spectrum_window():
    global spectrum_break_loop
    spectrum_break_loop = True

    def display_histogram(stdscr):
        global central_freq

        stdscr.clear()
        curses.curs_set(0)

        nfft = 1024
        fs = float(sample_rate)
        fc = float(central_freq)

        freqs = np.fft.fftfreq(nfft, 1 / fs)
        psd_values = np.fft.fft(driver.read(512), nfft)
        psd_values = np.abs(psd_values) ** 2 / nfft
        psd_values = 10 * np.log10(psd_values)

        psd_values = np.fft.fftshift(psd_values)
        freqs = np.fft.fftshift(freqs) + fc

        height, width = 20, 145
        height = min(height, 20)
        width = min(width, 145)

        min_psd = np.min(psd_values)
        max_psd = np.max(psd_values)

        num_bins = min(len(psd_values), width)
        scaled_psd = np.interp(psd_values, (min_psd, max_psd), (0, height - 1))

        for x in range(num_bins):
            column_height = int(scaled_psd[x])
            for y in range(height - column_height, height):
                stdscr.addch(y, x, curses.ACS_CKBOARD)

        for i in range(0, height - 1, 4):
            label = f"{int(min_psd + (max_psd - min_psd) * i / (height - 2))} dB"
            stdscr.addstr(height - i - 2, 0, label)

        for i in range(0, num_bins, 10):
            freq_label = f"{np.round(float(freqs[i]), 1)}MHz"
            stdscr.addstr(height - 1, i + 10 - len(freq_label) // 2, freq_label)

        stdscr.refresh()
        time.sleep(.1)

        key = stdscr.getch()
        if key != -1:
            if key == ord('q'):
                global spectrum_break_loop
                spectrum_break_loop = False

            elif key == (27 and 91 and 67):
                central_freq = central_freq + 1
                driver.set_central_freq(central_freq * 10e6)

            elif key == (27 and 91 and 68):
                central_freq = central_freq - 1
                driver.set_central_freq(central_freq * 10e6)

    main_screen.nodelay(True)
    while spectrum_break_loop:
        display_histogram(main_screen)

    main_screen.nodelay(False)


# endregion

# region [Waterfall]

waterfall_break_loop = True


def waterfall_window():
    global waterfall_break_loop
    main_screen.scrollok(True)

    num_colors = 2
    for i in range(1, num_colors):
        curses.init_pair(i, i, curses.COLOR_BLACK)

    def display_waterfall(stdscr):
        global central_freq

        stdscr.clear()
        curses.curs_set(0)

        nfft = 1024
        fs = float(sample_rate)
        fc = float(central_freq)

        min_psd, max_psd = -120, 0
        height, width = stdscr.getmaxyx()

        stdscr.clear()

        psd_values = np.fft.fft(driver.read(512), nfft)
        psd_values = np.abs(psd_values) ** 2 / nfft
        psd_values = 10 * np.log10(psd_values)

        psd_values = np.fft.fftshift(psd_values)

        num_bins = min(len(psd_values), width)

        scaled_psd = np.interp(psd_values, (min_psd, max_psd), (1, num_colors - 1))

        stdscr.scroll(1)
        stdscr.move(height - 1, 0)

        for x in range(num_bins):
            color_char = int(scaled_psd[x])
            if color_char >= num_colors:
                color_char = num_colors - 1
            elif color_char < 1:
                color_char = 1
            stdscr.addch(height - 1, x, ' ', curses.color_pair(color_char))

        stdscr.refresh()
        time.sleep(0.1)

        key = stdscr.getch()
        if key != -1:
            if key == ord('q'):
                global waterfall_break_loop
                waterfall_break_loop = False

            elif key == curses.KEY_RIGHT:
                central_freq = central_freq + 1
                driver.set_central_freq(central_freq * 10e6)

            elif key == curses.KEY_LEFT:
                central_freq = central_freq + 1
                driver.set_central_freq(central_freq * 10e6)

    main_screen.nodelay(True)
    while waterfall_break_loop:
        display_waterfall(main_screen)

    main_screen.nodelay(False)

# endregion


if __name__ == "__main__":
    main_window_generator()
