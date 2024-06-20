from front.CLI.cli_ver import *


def generate():
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

    actions = [lambda: rtl_setup(), None, lambda: spectrum_window(), lambda: waterfall_window(), None, lambda: summary_window()]

    window = Window([ActionOptions(1, 2, options, descriptions, actions, main_screen)], main_screen)
    window.draw()

    window.take_control()