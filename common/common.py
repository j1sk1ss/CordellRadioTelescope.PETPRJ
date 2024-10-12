import sys
import glob
import curses
import serial
import numpy as np

from operator import gt, lt
sys.path.append('/Users/nikolaj/CordellRadioTelescope.EXMPL/')
from driver.rtl2832u import RTL
from numpy.fft import fft, fftfreq


def perform_fft(data, sample_rate):
    n = len(data)
    yf = fft(data)
    xf = fftfreq(n, 1 / sample_rate)
    return xf, np.abs(yf)


def wrap_text(text, width):
    """
    Wrap text to fit within the given width and handle \n characters.
    """
    lines = []
    segments = text.split('\n')

    for segment in segments:
        while len(segment) > width:
            wrap_at = segment.rfind(' ', 0, width)
            if wrap_at == -1:
                wrap_at = width

            lines.append(segment[:wrap_at])
            segment = segment[wrap_at:].lstrip()

        lines.append(segment)

    return lines


def serial_ports():
    """
    Lists serial port names

    :raisesEnvironmentError:
        On unsupported or unknown platforms
    :returns:
        A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass

    return result


def frange3(start, stop, step):
    res, n = start, 0.
    predicate = lt if start < stop else gt
    while predicate(res, stop):
        yield res
        res = start + n * step
        n += 1


def spectro_analyze(rate, center, nfft=1024):
    import front.config

    frequencies = np.fft.fftfreq(nfft, 1 / rate)
    psd_values = np.fft.fft(front.config.rtl_driver.read(front.config.rtl_driver.sample_count), nfft)
    psd_values = np.abs(psd_values) ** 2 / nfft
    psd_values = 10 * np.log10(psd_values)

    psd_values = np.fft.fftshift(psd_values)
    frequencies = np.fft.fftshift(frequencies) + center

    return psd_values, frequencies


def check_rtl(scr, h, w):
    import front.config

    if not isinstance(front.config.rtl_driver, RTL):
        scr.screen.border()
        scr.screen.addstr(h // 2, w // 2, 'RTL not connected')
        scr.screen.addstr(h // 2 + 1, w // 2, 'q - exit | d - use stm32 dac value')
        scr.screen.refresh()
        scr.screen.nodelay(False)

        key = scr.screen.getch()
        if key == ord('q'):
            scr.looped = False
            return -1
        elif key == ord('d'):
            return 1
        else:
            scr.looped = False
            return -1

    return 0


def init_colors():
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

    return char_colors, brightness_chars
