import curses
import time
import numpy as np
import pandas as pd

from overrides import overrides

import front.config
from common.common import frange3, spectro_analyze, check_rtl, init_colors
from front.windows.window import Menu

degrees = 0
azimuth = 0
values = []


class MoveWin(Menu):
    @overrides
    def generate(self):
        self.screen.clear()

        h, w = 15, 60
        max_y, max_x = self.screen.getmaxyx()
        max_y, max_x = max_y - 1, max_x - 1

        waterfall_win = self.screen.subwin(h, w, 1, 0)
        spectrum_win = self.screen.subwin(h, w, 1, w)

        spectrum_win.clear()
        waterfall_win.clear()
        waterfall_win.scrollok(True)

        char_colors, brightness_chars = init_colors()

        current_values = []

        def display_movement_window():
            display_waterfall_win(h, w)
            display_histogram_win(h, w)

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

            global degrees, azimuth, values
            degree_pos = int(((degrees % 360) / 360) * scale_width)

            self.screen.addstr(scale_start_y - 1, scale_start_x + degree_pos + 1, "  ")
            self.screen.addstr(scale_start_y - 1, scale_start_x + degree_pos - 1, "  ")

            self.screen.addstr(scale_start_y - 1, scale_start_x + degree_pos, "\/")
            self.screen.addstr(scale_start_y + 1, scale_start_x, f"Degrees: {degrees:.1f} | Azimuth: {azimuth:.1f}")
            self.screen.addstr(
                max_y, 1,
                "<- | \/ - turn lower | s - snapshot | v - save value | "
                "a - lower freq. | d - upper freq. | /\ - turn upper | ->"
            )

            key = self.screen.getch()
            if key != -1:
                if key == ord('q'):
                    self.looped = False
                elif key == ord('v'):
                    current_values.append({
                        'degrees': degrees,
                        'value': np.average(front.config.stm32_driver.read(256))
                    })
                elif key == ord('s'):
                    summary = {
                        'powers': [],
                        'freq': []
                    }

                    for i in frange3(400.0, 1766.0, front.config.rtl_driver.body.sample_rate / 1e6):
                        psd_values, frequencies = spectro_analyze(
                            front.config.rtl_driver.body.sample_rate, float(i * 1e6), 64
                        )

                        summary['powers'].extend(psd_values)
                        summary['freq'].extend(frequencies)

                    pd.DataFrame(summary).to_csv(f'snap_in_{degrees:.1f}_{azimuth:.1f}.csv', index=False)

                elif key == (27 and 91 and 67):
                    degrees += 1.8
                elif key == (27 and 91 and 68):
                    degrees -= 1.8
                elif key == ord('d'):
                    front.config.rtl_driver.change_central_freq(1e6)
                elif key == ord('a'):
                    front.config.rtl_driver.change_central_freq(-1e6)
                if key == (27 and 91 and 65):
                    azimuth -= 1
                    if len(current_values) > 0:
                        values.append({
                            'azimuth': azimuth,
                            'values': current_values
                        })
                elif key == (27 and 91 and 66):
                    azimuth += 1
                    if len(current_values) > 0:
                        values.append({
                            'azimuth': azimuth,
                            'values': current_values
                        })

        def display_histogram_win(height, width):
            import front.config
            spectrum_win.clear()
            if check_rtl(self, height, width) == -1:
                return
            else:
                pass

            psd_values, frequencies = spectro_analyze(
                float(front.config.rtl_driver.body.get_sample_rate()), float(front.config.rtl_driver.get_central_freq())
            )

            min_psd = np.min(psd_values)
            max_psd = np.max(psd_values)

            num_bins = min(len(psd_values), width)
            scaled_psd = np.interp(psd_values, (min_psd, max_psd), (0, height - 1))

            for x in range(num_bins):
                column_height = int(scaled_psd[x])
                for y in range(height - column_height, height - 1):
                    spectrum_win.addch(y, x, curses.ACS_CKBOARD)

            spectrum_win.border()

            for i in range(0, height - 1, 4):
                label = f"{int(min_psd + (max_psd - min_psd) * i / (height - 2))}dB"
                spectrum_win.addstr(height - i - 2, 0, label)

            spectrum_win.refresh()
            time.sleep(front.config.rtl_driver.update_delay / 2)

        def display_waterfall_win(height, width):
            import front.config

            if check_rtl(self, height, width) == -1:
                return
            else:
                pass

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
                freq_label = f"{(fc - fs / 2 + (i / num_bins) * fs) / 1e6:.1f}"
                waterfall_win.addstr(height - 1, i + 1, freq_label[:4])

            waterfall_win.refresh()
            time.sleep(front.config.rtl_driver.update_delay / 2)

        self.screen.nodelay(True)
        self.looped = True
        self.loop(display_movement_window)
        self.screen.nodelay(False)
        self.screen.scrollok(False)

        curses.use_default_colors()
