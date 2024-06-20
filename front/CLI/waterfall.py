from front.CLI.cli_ver import *


waterfall_break_loop = True


def generate():
    import front.CLI.cli_ver

    front.CLI.cli_ver.main_screen.clear()

    global waterfall_break_loop
    waterfall_break_loop = True

    front.CLI.cli_ver.main_screen.scrollok(True)

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

    def display_waterfall(stdscr):
        nfft = 1024
        fs = float(front.CLI.cli_ver.sample_rate)
        fc = float(front.CLI.cli_ver.central_freq)

        min_psd, max_psd = -120, 0
        height, width = stdscr.getmaxyx()

        psd_values = np.fft.fft(front.CLI.cli_ver.driver.read(512), nfft)
        psd_values = np.abs(psd_values) ** 2 / nfft
        psd_values = 10 * np.log10(psd_values)
        psd_values = np.fft.fftshift(psd_values)

        num_bins = min(len(psd_values), width - 2)

        scaled_psd = np.interp(psd_values, (min_psd, max_psd), (0, len(brightness_chars) - 1))

        stdscr.setscrreg(0, height - 1)
        stdscr.scroll()
        stdscr.move(height - 2, 1)

        for x in range(num_bins):
            brightness_char = brightness_chars[int(scaled_psd[x])]
            stdscr.addch(height - 2, x + 1, brightness_char, char_colors[brightness_char])

        stdscr.border()
        
        for i in range(0, num_bins, width // 10):
            freq_label = f"{(fc - fs / 2 + (i / num_bins) * fs):.1f}"
            stdscr.addstr(height - 1, i + 1, freq_label[:4])

        stdscr.refresh()
        time.sleep(0.1)

        key = stdscr.getch()
        if key != -1:
            if key == ord('q'):
                global waterfall_break_loop
                waterfall_break_loop = False

            elif key == (27 and 91 and 67):
                front.CLI.cli_ver.central_freq += 1
                front.CLI.cli_ver.driver.set_central_freq(front.CLI.cli_ver.central_freq * 10e6)

            elif key == (27 and 91 and 68):
                front.CLI.cli_ver.central_freq -= 1
                front.CLI.cli_ver.driver.set_central_freq(front.CLI.cli_ver.central_freq * 10e6)

    front.CLI.cli_ver.main_screen.nodelay(True)
    while waterfall_break_loop:
        display_waterfall(front.CLI.cli_ver.main_screen)

    front.CLI.cli_ver.main_screen.nodelay(False)