import curses
import time
import numpy as np

from overrides import overrides
from front.windows.window import Menu


class Spectrum(Menu):
    @overrides
    def generate(self):
        self.looped = True

        def display_histogram():
            import front.config
            
            self.screen.clear()
            curses.curs_set(0)

            nfft = 1024
            fs = float(front.config.rtl_driver.body.sample_rate)
            fc = float(front.config.rtl_driver.body.center_freq)

            freqs = np.fft.fftfreq(nfft, 1 / fs)
            psd_values = np.fft.fft(front.config.rtl_driver.read(512), nfft)
            psd_values = np.abs(psd_values) ** 2 / nfft
            psd_values = 10 * np.log10(psd_values)

            psd_values = np.fft.fftshift(psd_values)
            freqs = np.fft.fftshift(freqs) + fc

            height, width = self.screen.getmaxyx()
            height, width = height - 1, width - 1

            min_psd = np.min(psd_values)
            max_psd = np.max(psd_values)

            num_bins = min(len(psd_values), width)
            scaled_psd = np.interp(psd_values, (min_psd, max_psd), (0, height - 1))

            for x in range(num_bins):
                column_height = int(scaled_psd[x])
                for y in range(height - column_height, height):
                    self.screen.addch(y, x, curses.ACS_CKBOARD)

            self.screen.border()

            for i in range(0, height - 1, 4):
                label = f"{int(min_psd + (max_psd - min_psd) * i / (height - 2))} dB"
                self.screen.addstr(height - i - 2, 0, label)

            for i in range(0, num_bins, 10):
                freq_label = f"{np.round(float(freqs[i] / 10e6), 1)}mHz"
                self.screen.addstr(height - 1, i + 10 - len(freq_label) // 2, freq_label)

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
        self.loop(display_histogram)
        self.screen.nodelay(False)
