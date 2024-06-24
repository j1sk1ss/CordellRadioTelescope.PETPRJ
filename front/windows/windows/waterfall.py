import curses
import time
import numpy as np

from overrides import overrides
from front.windows.window import Menu


class Waterfall(Menu):
    @overrides
    def generate(self):
        import front.config

        self.screen.clear()
        self.looped = True

        self.screen.scrollok(True)

        brightness_chars = " .:-=+*#%@"

        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
        curses.init_pair(2, curses.COLOR_CYAN, curses.COLOR_BLACK)
        curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        curses.init_pair(5, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
        curses.init_pair(6, curses.COLOR_RED, curses.COLOR_BLACK)

        char_colors = {
            " ": curses.color_pair(1),  # blue
            ".": curses.color_pair(1),  # blue
            ":": curses.color_pair(2),  # cyan
            "-": curses.color_pair(2),  # cyan
            "=": curses.color_pair(3),  # green
            "+": curses.color_pair(3),  # green
            "*": curses.color_pair(4),  # yellow
            "#": curses.color_pair(5),  # magenta
            "%": curses.color_pair(5),  # magenta
            "@": curses.color_pair(6),  # red
        }

        def display_waterfall():
            nfft = 1024
            fs = float(front.config.rtl_driver.body.sample_rate)
            fc = float(front.config.rtl_driver.body.center_freq)

            min_psd, max_psd = -120, 0
            height, width = self.screen.getmaxyx()

            psd_values = np.fft.fft(front.config.rtl_driver.read(512), nfft)
            psd_values = np.abs(psd_values) ** 2 / nfft
            psd_values = 10 * np.log10(psd_values)
            psd_values = np.fft.fftshift(psd_values)

            num_bins = min(len(psd_values), width - 2)

            scaled_psd = np.interp(psd_values, (min_psd, max_psd), (0, len(brightness_chars) - 1))

            self.screen.setscrreg(0, height - 1)
            self.screen.scroll()
            self.screen.move(height - 2, 1)

            for x in range(num_bins):
                brightness_char = brightness_chars[int(scaled_psd[x])]
                self.screen.addch(height - 2, x + 1, brightness_char, char_colors[brightness_char])

            self.screen.border()

            for i in range(0, num_bins, width // 10):
                freq_label = f"{(fc - fs / 2 + (i / num_bins) * fs) / 10e6:.1f}"
                self.screen.addstr(height - 1, i + 1, freq_label[:4])

            self.screen.refresh()
            time.sleep(front.config.rtl_driver.update_delay)

            key = self.screen.getch()
            if key != -1:
                if key == ord('q'):
                    self.looped = False

                elif key == (27 and 91 and 67):
                    front.config.rtl_driver.body.center_freq += 10e6

                elif key == (27 and 91 and 68):
                    front.config.rtl_driver.body.center_freq -= 10e6

        self.screen.nodelay(True)
        self.loop(display_waterfall)

        curses.start_color()
        self.screen.nodelay(False)
        self.screen.scrollok(False)
