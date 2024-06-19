import colorama
from colorama import Fore, Back, Style
import pyfiglet
import os

colorama.init()


class OptionGenerator:
    def __init__(self, options, descriptions, actions):
        self.options = options
        self.descriptions = descriptions
        self.actions = actions

    def draw_options(self):
        for option in self.options:
            print(option)

    def read_input(self, key):
        if key.isdigit() and 0 <= int(key) < len(self.actions):
            self.actions[int(key)]()


class ProgramWindow:
    def __init__(self, background):
        self.drop_samples = None
        self.max_buffer = None
        self.agc_mode = None
        self.tuner_gain = None
        self.sample_rate = None
        self.central_freq = None
        self.com_port = None
        
        self._background = background
        self.clear_screen(background)

    def draw_main_window(self):
        options = OptionGenerator(
            ["0) RTL-SDR setup", "1) XY setup", "2) Spectrum", "3) Waterfall", "4) Movement", "5) Summary"],
            [
                "This window will give interface for setting RTL-SDR COM-port. In different OS COM-ports named differently. You should do this as the first step.",
                "XY setup needed when you have a navigation system of two or more motors. There you can choose COM-port, power, and other stuff.",
                "Spectrum analyzer window shows the spectrum in real-time. RTL-SDR sends data by serial port to Cordell RSA, then Cordell RSA draws graphs of the spectrum.",
                "Waterfall window is the second part of the spectrum window. Every second this window draws a line of spectrum, stores it, and moves it down. With this window, you can find blinking signals.",
                "XY movement window for working with your navigation system. Don't forget to check the XY setup window.",
                "Summary window includes data about authors and a simple guide on how to create your own radiotelescope."
            ],
            [self.draw_rtl_setup_window, self.draw_xy_setup_window, self.draw_spectrum_window, self.draw_waterfall_window, self.draw_movement_window, self.draw_summary_window]
        )

        while True:
            print(Fore.GREEN + Style.BRIGHT + "Cordell RSA program. Credits: j1sk1ss" + Style.RESET_ALL)
            print(pyfiglet.figlet_format("Cordell RSA"))
            print("\n" * 5)

            options.draw_options()
            key = input("Choose an option: ")

            options.read_input(key)

            self.clear_screen(Fore.WHITE)

    def draw_rtl_setup_window(self):
        self.clear_screen(Fore.WHITE)

        options = OptionGenerator(
            [
                f"0) COM-port <{self.com_port}>",
                f"1) Center frequency <{self.central_freq} mHz>",
                f"2) Sample rate <{self.sample_rate} mHz>",
                f"3) Tuner gain mode <{self.tuner_gain}>",
                f"4) AGC mode <{self.agc_mode}>",
                f"5) Max async buffer size <{self.max_buffer}>",
                f"6) Drop samples on full buffer <{self.drop_samples}>"
            ],
            None,
            [self.set_rtl_port, self.set_central_freq, self.set_sample_rate, self.set_tuner_gain, self.set_agc_mode, self.set_max_buffer, self.set_drop_sample]
        )

        while True:
            print(Fore.GREEN + Style.BRIGHT + "RTL setup" + Style.RESET_ALL)
            print("\n" * 17)

            options.draw_options()

            key = input("Choose an option (or press Enter to go back): ")

            if key == "":
                break
            options.read_input(key)

            self.clear_screen(Fore.WHITE)

        self.draw_rtl_setup_window()

    def set_rtl_port(self):
        self.com_port = input("Type number of port: ")

    def set_central_freq(self):
        self.central_freq = input("Set central freq: ")

    def set_sample_rate(self):
        self.sample_rate = input("Set sample rate: ")

    def set_tuner_gain(self):
        self.tuner_gain = input("New tuner gain: ")

    def set_agc_mode(self):
        self.agc_mode = input("New AGC mode: ")

    def set_max_buffer(self):
        self.max_buffer = input("Set buffer size: ")

    def set_drop_sample(self):
        self.drop_samples = input("Drop samples (True / False): ")

    def draw_xy_setup_window(self):
        print(Fore.GREEN + Style.BRIGHT + "XY setup" + Style.RESET_ALL)
        # Implement the XY setup window here

    def draw_spectrum_window(self):
        print(Fore.GREEN + Style.BRIGHT + "Radio Spectrum Analyzer" + Style.RESET_ALL)
        # Implement the Spectrum window here

    def draw_waterfall_window(self):
        print(Fore.GREEN + Style.BRIGHT + "Waterfall Analyzer" + Style.RESET_ALL)
        # Implement the Waterfall window here

    def draw_movement_window(self):
        print(Fore.GREEN + Style.BRIGHT + "Movement manager" + Style.RESET_ALL)
        # Implement the Movement window here

    def draw_summary_window(self):
        print(Fore.GREEN + Style.BRIGHT + "Summary" + Style.RESET_ALL)
        # Implement the Summary window here

    def clear_screen(self, color):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(color, end='')


if __name__ == "__main__":
    window = ProgramWindow(Back.WHITE)
    window.draw_main_window()
