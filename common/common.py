import glob
import sys

import numpy as np
import serial
from numpy.fft import fft, fftfreq

from operator import gt, lt


def perform_fft(data, sample_rate):
    n = len(data)
    yf = fft(data)
    xf = fftfreq(n, 1 / sample_rate)
    return xf, np.abs(yf)


def wrap_text(text, width):
    """
    Wrap text to fit within the given width and handle \n characters.
    """
    lines    = []
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

    :raises EnvironmentError:
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
