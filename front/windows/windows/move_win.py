import curses
import time
import numpy as np
import pandas as pd

from overrides import overrides

import front.config
from common.common import frange3, spectro_analyze
from front.windows.window import Menu


degrees = 0
azimuth = 0


class MoveWin(Menu):
    @overrides
    def generate(self):
        self.screen.clear()

        h, w = 15, 70
        max_y, max_x = self.screen.getmaxyx()
        max_y, max_x = max_y - 1, max_x - 1

        waterfall_win = self.screen.subwin(h, w, 1, (max(max_x - w, 0)) // 2)

        waterfall_win.clear()
        waterfall_win.scrollok(True)

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

        def display_movement_window():
            display_waterfall_win(h, w)

            scale_height = 3
            scale_width = max_x - 2
            scale_start_y = max_y - scale_height - 1
            scale_start_x = 1

            scale_str = "|"
            for i in range(0, scale_width):
                if i % 10 == 0:
                    scale_str += "|"
                else:
                    scale_str += "."

            self.screen.addstr(scale_start_y, scale_start_x, scale_str)

            global degrees, azimuth
            degree_pos = int(((degrees % 360) / 360) * scale_width)

            self.screen.addstr(scale_start_y - 1, scale_start_x + degree_pos + 1, "  ")
            self.screen.addstr(scale_start_y - 1, scale_start_x + degree_pos - 1, "  ")

            self.screen.addstr(scale_start_y - 1, scale_start_x + degree_pos, "\/")
            self.screen.addstr(scale_start_y + 1, scale_start_x, f"Degrees: {degrees:.1f} | Azimuth: {azimuth:.1f}")
            self.screen.addstr(max_y, 1, "<- | \/ - turn lower | s - snapshot | /\ - turn upper | ->")

            key = self.screen.getch()
            if key != -1:
                if key == ord('q'):
                    self.looped = False
                elif key == ord('s'):
                    summary = {
                        'powers': [],
                        'freq': []
                    }

                    for i in frange3(400.0, 1766.0, front.config.rtl_driver.body.sample_rate / 10e6):
                        psd_values, frequencies = spectro_analyze(
                            front.config.rtl_driver.body.sample_rate, float(i * 10e6), 64
                        )

                        summary['powers'].extend(psd_values)
                        summary['freq'].extend(frequencies)

                    pd.DataFrame(summary).to_csv(f'snap_in_{degrees:.1f}_{azimuth:.1f}.csv')

                elif key == (27 and 91 and 67):
                    degrees += 1.8
                elif key == (27 and 91 and 68):
                    degrees -= 1.8
                if key == (27 and 91 and 65):
                    azimuth -= 1
                elif key == (27 and 91 and 66):
                    azimuth += 1

        def display_waterfall_win(height, width):
            import front.config

            nfft = 1024
            fs = float(front.config.rtl_driver.body.sample_rate)
            fc = float(front.config.rtl_driver.body.center_freq)

            min_psd, max_psd = -120, 0

            psd_values = np.fft.fft(front.config.rtl_driver.read(512), nfft)
            psd_values = np.abs(psd_values) ** 2 / nfft
            psd_values = 10 * np.log10(psd_values)
            psd_values = np.fft.fftshift(psd_values)

            num_bins = min(len(psd_values), width - 2)

            scaled_psd = np.interp(psd_values, (min_psd, max_psd), (0, len(brightness_chars) - 1))

            waterfall_win.setscrreg(0, height - 2)
            waterfall_win.scroll()
            waterfall_win.move(height - 2, 1)

            for x in range(num_bins):
                brightness_char = brightness_chars[int(scaled_psd[x])]
                waterfall_win.addch(height - 2, x + 1, brightness_char, char_colors[brightness_char])

            waterfall_win.border()

            for i in range(0, num_bins, width // 10):
                freq_label = f"{(fc - fs / 2 + (i / num_bins) * fs) / 10e6:.1f}"
                waterfall_win.addstr(height - 1, i + 1, freq_label[:4])

            waterfall_win.refresh()
            time.sleep(front.config.rtl_driver.update_delay)

        self.screen.nodelay(True)
        self.looped = True
        self.loop(display_movement_window)
        self.screen.nodelay(False)
        self.screen.scrollok(False)

        curses.use_default_colors()
