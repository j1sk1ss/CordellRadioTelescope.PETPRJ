import curses

from driver.driver import Driver
from driver.rtl2832u import RTL
from front.CLI.windows.components.options import ActionOptions
from front.CLI.windows.window import Window


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

    actions = [lambda: rtl_setup_window(), None, None, None, None, None]

    window = Window([ActionOptions(1, 2, options, descriptions, actions, main_screen)], main_screen)
    window.draw()

    window.take_control()


# endregion

# region [RTL setup]

com_port = '0'
central_freq = '1420'
sample_rate = '2'
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
        f"Enabled devices: \n{str(RTL.get_serials())}",
        "The center frequency that the receiver is tuned to. Specify the value in MHz.",
        "The sampling rate for capturing signals. Specify the value in MHz.",
        "The tuner gain mode. Choose the mode that controls the gain level for signal reception.",
        "Count of samples",
        "<EXIT>"
    ]

    # region [RTL win handlers]

    def com(body: ActionOptions, data):
        global com_port, driver

        com_port = data
        body.options[0] = f"0) COM-port <{com_port}>"

        driver = RTL(com_port)

        main_screen.refresh()

    def cfreq(body: ActionOptions, data):
        global central_freq, driver
        central_freq = data
        body.options[1] = f"1) Center frequency <{central_freq} mHz>"

        driver.set_central_freq(central_freq)

        main_screen.refresh()

    def srate(body: ActionOptions, data):
        global sample_rate, driver
        sample_rate = data
        body.options[2] = f"2) Sample rate <{sample_rate} mHz>"

        driver.set_sample_rate(sample_rate)

        main_screen.refresh()

    def tuner(body: ActionOptions, data):
        global tuner_gain, driver
        tuner_gain = data
        body.options[3] = f"3) Tuner gain mode <{tuner_gain}>"

        driver.set_gain(tuner_gain)

        main_screen.refresh()

    def scount(body: ActionOptions, data):
        global sample_count, driver
        sample_count = data
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


if __name__ == "__main__":
    main_window_generator()
