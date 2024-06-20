import numpy as np
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
