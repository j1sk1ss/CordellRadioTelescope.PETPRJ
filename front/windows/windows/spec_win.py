import curses
import time
import numpy as np

from overrides import overrides

from common.common import frange3, spectro_analyze, check_rtl
from front.windows.components.options import ActionOptions
from front.windows.components.text import Text
from front.windows.window import Menu, Window


min_freq = 0.0
max_freq = 0.1
freq_step = 2.0
line_width = 2.048
difference = 10.0
chosen_freq = 0


class Spectrum(Menu):
    @overrides
    def generate(self):
        self.looped = True

# region [Finder]

# region [Finder handlers]

        def set_min(body: ActionOptions, data):
            global min_freq
            min_freq = float(data)
            body.options[0] = f"0) Min freq. <{min_freq} mHz>"
            self.screen.refresh()

        def set_max(body: ActionOptions, data):
            global max_freq
            max_freq = float(data)
            body.options[1] = f"1) Max freq. <{max_freq} mHz>"
            self.screen.refresh()

        def set_freqs(body: ActionOptions, data):
            global freq_step
            freq_step = float(data)
            body.options[2] = f"2) Step <{freq_step} mHz>"
            self.screen.refresh()

        def set_linew(body: ActionOptions, data):
            global line_width
            line_width = float(data)
            body.options[3] = f"3) Line width <{line_width} mHz>"
            self.screen.refresh()

        def set_diff(body: ActionOptions, data):
            global difference
            difference = float(data)
            body.options[4] = f"4) Difference <{difference} dB>"
            self.screen.refresh()

# region [Analyze results]

        def astart(body: ActionOptions):
            data = []
            summary = []

            for i in frange3(min_freq, max_freq, freq_step):
                psd_values, frequencies = spectro_analyze(
                    line_width * 1e6, float(i * 1e6)
                )

                summary.extend(psd_values)
                average = np.mean(psd_values)
                for j in range(len(psd_values)):
                    power = psd_values[j]
                    frequency = frequencies[j]

                    if abs(abs(power) - abs(average)) > difference:
                        data.append({
                            'freq': frequency,
                            'power': power,
                            'average': average
                        })

            exit_code = display_results(data, summary)
            if exit_code == -1:
                pass
            elif exit_code == 10:
                self.action = display_histogram
                body.parent.untie()
                self.screen.nodelay(True)

        def display_results(data, summary):
            self.screen.clear()
            max_y, max_x = self.screen.getmaxyx()
            max_y -= 2
            max_x -= 2
            self.screen.border()

            col_width = max_x // 2
            max_rows = max_y - 2

            def draw_page(start_index, cpos):
                self.screen.clear()
                self.screen.border()
                self.screen.addstr(0, 2, "Summary of PSD Values:")
                y = 1
                for i, value in enumerate(summary[start_index:start_index + max_rows // 2]):
                    self.screen.addstr(y, 2, f"Power: {value:.2f} dB")
                    y += 1

                y = 1
                col = col_width + 2
                self.screen.addstr(0, col, "Interested freq.:")
                for i, entry in enumerate(data[start_index:start_index + max_rows // 2]):
                    if cpos == y:
                        global chosen_freq
                        chosen_freq = entry['freq']
                        self.screen.addstr(y, col,
                                           f"Freq: {entry['freq'] / 1e6:.2f} MHz, "
                                           f"Power: {entry['power']:.2f}dB / {entry['average']:.2f}dB", curses.A_REVERSE
                                           )
                    else:
                        self.screen.addstr(y, col,
                                           f"Freq: {entry['freq'] / 1e6:.2f} MHz, "
                                           f"Power: {entry['power']:.2f}dB / {entry['average']:.2f}dB")
                    y += 1

                self.screen.refresh()

            index = 0
            cursor = 0
            draw_page(index, cursor)

            while True:
                key = self.screen.getch()
                if key == (27 and 91 and 65) and cursor >= 0:
                    cursor -= 1
                    if cursor < 0:
                        index -= max_rows // 2
                        cursor = max_rows // 2
                elif key == (27 and 91 and 66) and index + max_rows // 2 < len(summary):
                    cursor += 1
                    if cursor >= max_rows // 2:
                        index += max_rows // 2
                        cursor = 0
                elif key == 10:
                    global chosen_freq

                    import front.config
                    front.config.rtl_driver.set_central_freq(chosen_freq)

                    return 10
                elif key == ord('q'):
                    self.action = display_histogram
                    return -1

                draw_page(index, cursor)

# endregion

        def wexit(body: ActionOptions):
            body.parent.untie()
            self.parent.generate()

# endregion

        global min_freq, max_freq, freq_step, line_width, difference
        finder_window = Window(
            [
                Text('Finder - simple tool for spectrum analyze. Set max freq., min freq., step and width of line. '
                     'Then set interested difference with average value. After analyze, you will receive list '
                     'of signals. Good luck!', 0, 0),
                ActionOptions(0, 3, [
                    f"0) Min freq. <{min_freq} mHz>", f"1) Max freq. <{max_freq} mHz>",
                    f"2) Step <{freq_step} mHz>", f"3) Line width <{line_width} mHz>",
                    f"4) Difference <{difference} dB>", f"5) Start analyze", f"6) Exit"
                ], [
                    "Minimal frequency of spectrum that will be analyzed. For example, "
                    "spectrum between 0 mHz and 1500 mHz, has 0 mHz as minimum frequency.",
                    "Maximal frequency of spectrum that will be analyzed. For example, "
                    "spectrum between 0 mHz and 1500 mHz, has 1500 mHz as maximum frequency.",
                    "Step - spectrum that will be skipped. For example, spectrum between 0 mHz and 1500 mHz "
                    "with 0 mHz step will produce analyze of 1500 bins. With 2 mHz step - analyze of 750 bins.",
                    "Line width - count of bins that will united into larger bin.",
                    "Difference - difference bin value in line with average of this bin.",
                    "<START>", "<EXIT>"
                ], [
                    set_min, set_max, set_freqs, set_linew, set_diff, astart, wexit
                ])
            ], self.screen
        )

        def display_finder():
            self.screen.nodelay(False)
            finder_window.draw()
            finder_window.take_control()

# endregion

# region [Histogram]

# region [STM32]

        def display_stm32_value():
            import front.config

            self.screen.clear()
            curses.curs_set(0)

            height, width = self.screen.getmaxyx()
            height, width = height - 2, width - 1

            self.screen.border()
            self.screen.addstr(height // 2, width // 2, f'Value: {np.mean(front.config.stm32_driver.read(256))}')
            self.screen.addstr(height + 1, 0, 'q - exit')

            self.screen.refresh()
            time.sleep(0.05)

            key = self.screen.getch()
            if key != -1:
                if key == ord('q'):
                    self.looped = False
                    front.config.stm32_driver.send('m\n')

# endregion

        def display_histogram():
            import front.config

            self.screen.clear()
            curses.curs_set(0)

            height, width = self.screen.getmaxyx()
            height, width = height - 2, width - 1

            code = check_rtl(self, height, width)
            if code == -1:
                return
            elif code == 1:
                self.screen.nodelay(True)
                front.config.stm32_driver.send('a\n')
                self.action = display_stm32_value
                return

            psd_values, frequencies = spectro_analyze(
                float(front.config.rtl_driver.body.get_sample_rate()), float(front.config.rtl_driver.get_central_freq())
            )

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
                label = f"{int(min_psd + (max_psd - min_psd) * i / (height - 2))}dB"
                self.screen.addstr(height - i - 2, 0, label)

            for i in range(0, num_bins, 10):
                freq_label = f"{np.round(float(frequencies[i] / 1e6), 1)}mHz"
                self.screen.addstr(height - 1, i + 10 - len(freq_label) // 2, freq_label)

            self.screen.addstr(height + 1, 0, f'q - exit | e - finder interface')
            self.screen.refresh()
            time.sleep(front.config.rtl_driver.update_delay)

            key = self.screen.getch()
            if key != -1:
                if key == ord('q'):
                    self.looped = False
                elif key == ord('e'):
                    self.action = display_finder
                elif key == (27 and 91 and 67):
                    front.config.rtl_driver.change_central_freq(1e6)
                elif key == (27 and 91 and 68):
                    front.config.rtl_driver.change_central_freq(-1e6)

        # endregion

        self.screen.nodelay(True)
        self.loop(display_histogram)
        self.screen.nodelay(False)
