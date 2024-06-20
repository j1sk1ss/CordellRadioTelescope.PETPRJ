from front.CLI.cli_ver import *


spectrum_break_loop = True


def generate():
    import front.CLI.cli_ver

    global spectrum_break_loop
    spectrum_break_loop = True

    def display_histogram(stdscr):
        stdscr.clear()
        curses.curs_set(0)

        nfft = 1024
        fs = float(front.CLI.cli_ver.sample_rate)
        fc = float(front.CLI.cli_ver.central_freq)

        freqs = np.fft.fftfreq(nfft, 1 / fs)
        psd_values = np.fft.fft(front.CLI.cli_ver.driver.read(512), nfft)
        psd_values = np.abs(psd_values) ** 2 / nfft
        psd_values = 10 * np.log10(psd_values)

        psd_values = np.fft.fftshift(psd_values)
        freqs = np.fft.fftshift(freqs) + fc

        height, width = stdscr.getmaxyx()
        height, width = height - 1, width - 1

        min_psd = np.min(psd_values)
        max_psd = np.max(psd_values)

        num_bins = min(len(psd_values), width)
        scaled_psd = np.interp(psd_values, (min_psd, max_psd), (0, height - 1))

        for x in range(num_bins):
            column_height = int(scaled_psd[x])
            for y in range(height - column_height, height):
                stdscr.addch(y, x, curses.ACS_CKBOARD)

        stdscr.border()

        for i in range(0, height - 1, 4):
            label = f"{int(min_psd + (max_psd - min_psd) * i / (height - 2))} dB"
            stdscr.addstr(height - i - 2, 0, label)

        for i in range(0, num_bins, 10):
            freq_label = f"{np.round(float(freqs[i]), 1)}mHz"
            stdscr.addstr(height - 1, i + 10 - len(freq_label) // 2, freq_label)

        stdscr.refresh()
        time.sleep(.1)

        key = stdscr.getch()
        if key != -1:
            if key == ord('q'):
                global spectrum_break_loop
                spectrum_break_loop = False

            elif key == (27 and 91 and 67):
                front.CLI.cli_ver.central_freq += 1.0
                front.CLI.cli_ver.driver.set_central_freq(front.CLI.cli_ver.central_freq * 10e6)

            elif key == (27 and 91 and 68):
                front.CLI.cli_ver.central_freq -= 1.0
                front.CLI.cli_ver.driver.set_central_freq(front.CLI.cli_ver.central_freq * 10e6)

    front.CLI.cli_ver.main_screen.nodelay(True)
    while spectrum_break_loop:
        display_histogram(front.CLI.cli_ver.main_screen)

    front.CLI.cli_ver.main_screen.nodelay(False)