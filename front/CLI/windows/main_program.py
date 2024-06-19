import curses

from components.options import ActionOptions
from window import Window


main_screen = curses.initscr()


# region [Main]

def main_window_generator():
    options = [
        "0) RTL-SDR setup", "1) XY setup", "2) Spectrum", "3) Waterfall", "4) Movement", "5) Summary"
        ]
    
    descriptions = [
        "This window will give interface for setting RTL-SDR COM-port. In different OS COM-ports named differend. You should do this as first step.",
        "XY setup needed when you have navigation system of two or more motors. There you can choose COM-port, power and other stuff.",
        "Spectrum analyzer window show spectrum in real time. RTL-SDR send data by serial port to Cordell RSA, then Cordell RSA draw graphs of spectrum.",
        "Waterfall window is a second part of spectrum window. Every second whis window draws line of spectrum, store, and move it down. With this window you can find blinking sighnal.",
        "XY movement window for working with your navigation system. Don`t forget check XY setup window.",
        "Summary window includes data about authors and simple guide how to create your own radiotelescope"
        ]
    
    actions = [lambda: rtl_setup_window(), None, None, None, None, None]

    window = Window([ActionOptions(1, 2, options, descriptions, actions, main_screen)], main_screen)
    window.draw()

    window.take_control()

# endregion

# region [RTL setup]

com_port = ''
central_freq = ''
sample_rate = ''
tuner_gain = ''
agc_mode = ''
max_buffer = ''
drop_samples = ''

def rtl_setup_window():
    options = [
        f"0) COM-port <{com_port}>", f"1) Center frequency <{central_freq} mHz>", f"2) Sample rate <{sample_rate} mHz>",
        f"3) Tuner gain mode <{tuner_gain}>", f"4) AGC mode <{agc_mode}>", f"5) Max async buffer size <{max_buffer}>", f"6) Drop samples on full buffer <{drop_samples}>",
        "7) Exit"
        ]
    
    descriptions = [
        "The COM port used to communicate with the device. Specify the port number to which the device is connected.",
        "The center frequency that the receiver is tuned to. Specify the value in MHz.",
        "The sampling rate for capturing signals. Specify the value in MHz.",
        "The tuner gain mode. Choose the mode that controls the gain level for signal reception.",
        "Automatic Gain Control (AGC) mode. Enable or disable automatic gain adjustment to stabilize the signal level.",
        "The maximum size of the asynchronous buffer. Specify the buffer size for handling asynchronous data.",
        "Drop samples when the buffer is full. Enable or disable dropping data when the buffer overflows.", "<EXIT>"
        ]
    
    def com(data):
        global com_port
        com_port = data
        main_screen.refresh()
        
    def cfreq(data):
        global central_freq
        central_freq = data
        main_screen.refresh()
        
    def srate(data):
        global sample_rate
        sample_rate = data
        main_screen.refresh()
        
    def tuner(data):
        global tuner_gain
        tuner_gain = data
        main_screen.refresh()
        
    def agc(data):
        global agc_mode
        agc_mode = data
        main_screen.refresh()
        
    def buffer(data):
        global max_buffer
        max_buffer = data
        main_screen.refresh()
        
    def dsamples(data):
        global drop_samples
        drop_samples = data
        main_screen.refresh()
    
    actions = [com, cfreq, srate, tuner, agc, buffer, dsamples]
    
    window = Window([ActionOptions(1, 2, options, descriptions, actions, main_screen)], main_screen)
    window.draw()

    window.take_control()

# endregion


if __name__ == "__main__":
    main_window_generator()