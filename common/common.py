import numpy as np
from numpy.fft import fft, fftfreq


def perform_fft(data, sample_rate):
    n = len(data)
    yf = fft(data)
    xf = fftfreq(n, 1 / sample_rate)
    return xf, np.abs(yf)
