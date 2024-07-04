import curses
import time
import numpy as np
import pandas as pd

from overrides import overrides

import front.config
from common.common import frange3, spectro_analyze, check_rtl, init_colors
from driver.nema17 import Direction
from front.windows.components.border import Border
from front.windows.components.options import ActionOptions
from front.windows.components.text import Text
from front.windows.window import Menu, Window

degrees = 0
azimuth = 0
values = []

# region [Config vars]

resolution = 64
deg_per_step = 1.8
az_per_step = 1
lower_frequency = 500.0
upper_frequency = 1766.0


# endregion


class MoveWin(Menu):
    @overrides
    def generate(self):
        front.config.nema17_driver.turn_on()
        front.config.nema17_driver.disable()

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

        # region [Handlers]

        def snap_res(body: ActionOptions, data):
            global resolution
            resolution = int(data)
            body.options[0] = f"0) Snap resolution <{resolution}>"
            self.screen.refresh()

        def deg_step(body: ActionOptions, data):
            global deg_per_step
            deg_per_step = int(data)
            body.options[1] = f"1) Degrees per step <{deg_per_step}>"
            self.screen.refresh()

        def az_step(body: ActionOptions, data):
            global az_per_step
            az_per_step = int(data)
            body.options[2] = f"2) Azimuth per step <{az_per_step}>"
            self.screen.refresh()

        def lower(body: ActionOptions, data):
            global lower_frequency
            lower_frequency = float(data)
            body.options[3] = f"3) Lower freq. <{lower_frequency} mHz>"
            self.screen.refresh()

        def upper(body: ActionOptions, data):
            global upper_frequency
            upper_frequency = float(data)
            body.options[4] = f"4) Upper freq. <{upper_frequency} mHz>"
            self.screen.refresh()

        def wexit(body: ActionOptions):
            body.parent.untie()
            self.screen.nodelay(True)
            self.action = display_movement_window

        # endregion

        global resolution, deg_per_step, az_per_step, lower_frequency, upper_frequency

        config_window = Window(
            [
                Border(0, 0),
                Text('Configurations', 0, 0),
                ActionOptions(
                    1, 1,
                    [
                        f"0) Snap resolution <{resolution}>", f"1) Degrees per step <{deg_per_step}>",
                        f"2) Azimuth per step <{az_per_step}>", f"3) Lower freq. <{lower_frequency} mHz>",
                        f"4) Upper freq. <{upper_frequency} mHz>", "5) Exit"
                    ],
                    [
                        "<SNAP_RES>", "Degrees per one step", "Azimuth angle per one step",
                        "Lower bound of snapshot", "Upper bound of snapshot", "<EXIT>"
                    ],
                    [
                        snap_res, deg_step, az_step, lower, upper, wexit
                    ]
                )
            ], self.screen
        )

        def display_config_win():
            self.screen.nodelay(False)
            config_window.draw()
            config_window.take_control()

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

            self.screen.move(scale_start_y - 1, 0)
            self.screen.clrtoeol()

            self.screen.addstr(scale_start_y - 1, scale_start_x + degree_pos, "\/")
            self.screen.addstr(scale_start_y + 1, scale_start_x, f"Degrees: {degrees:.1f} | Azimuth: {azimuth:.1f}")
            self.screen.addstr(
                max_y, 1,
                "<- | \/ - turn lower | s - snapshot | v - save value | "
                "a - lower freq. | d - upper freq. | c - config | /\ - turn upper | ->"
            )

            key = self.screen.getch()
            if key != -1:
                if key == ord('q'):
                    self.looped = False
                if key == ord('c'):
                    self.action = display_config_win
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

                    for i in frange3(lower_frequency, upper_frequency, front.config.rtl_driver.body.sample_rate / 1e6):
                        front.config.rtl_driver.set_central_freq(i * 1e6)
                        psd_values, frequencies = spectro_analyze(
                            front.config.rtl_driver.body.sample_rate,
                            float(front.config.rtl_driver.get_central_freq()),
                            resolution
                        )

                        summary['powers'].extend(psd_values)
                        summary['freq'].extend(frequencies)

                    pd.DataFrame(summary).to_csv(f'snap_in_{degrees:.1f}_{azimuth:.1f}.csv', index=False)

                elif key == (27 and 91 and 67):
                    front.config.nema17_driver.move(deg_per_step, Direction.RIGHT, 25000)
                    degrees += deg_per_step

                elif key == (27 and 91 and 68):
                    front.config.nema17_driver.move(deg_per_step, Direction.LEFT, 25000)
                    degrees += deg_per_step

                elif key == ord('d'):
                    front.config.rtl_driver.change_central_freq(1e6)
                elif key == ord('a'):
                    front.config.rtl_driver.change_central_freq(-1e6)
                if key == (27 and 91 and 65):
                    azimuth -= az_per_step
                    if len(current_values) > 0:
                        values.append({
                            'azimuth': azimuth,
                            'values': current_values
                        })
                elif key == (27 and 91 and 66):
                    azimuth += az_per_step
                    if len(current_values) > 0:
                        values.append({
                            'azimuth': azimuth,
                            'values': current_values
                        })

        # region [Info wins]

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

        # endregion

        self.screen.nodelay(True)
        self.looped = True
        self.loop(display_movement_window)
        self.screen.nodelay(False)
        self.screen.scrollok(False)

        front.config.nema17_driver.turn_off()
        curses.use_default_colors()
