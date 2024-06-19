import matplotlib
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider

from common.common import perform_fft
from driver.stm32f103 import STM32

import numpy as np

matplotlib.use("TkAgg")


# region [Global vars]

MAX_FREQ = 100000
MIN_FREQ = -100000
MAX_DB = 1000
BANDWIDTH = MAX_FREQ - MIN_FREQ

controller = STM32()

waterfall_lim = 10
waterfall = []

# endregion


try:
    plt.ion()
    fig = plt.figure(figsize=(12, 10))

    ax1 = fig.add_subplot(211)
    ax2 = fig.add_subplot(212, projection='3d')

    # Initial center frequency
    center_freq = 0
    freq_range = (center_freq - BANDWIDTH // 2, center_freq + BANDWIDTH // 2)


    def update_plot(val):
        global center_freq, freq_range
        center_freq = slider.val
        freq_range = (center_freq - BANDWIDTH // 2, center_freq + BANDWIDTH // 2)
        update_graphs()


    def update_graphs():
        if not waterfall:
            return

        freq, spec = perform_fft(data, 1000000)

        ax1.cla()
        ax1.plot(freq, spec)
        ax1.set_title('Cordell Spectrum Analyzer')
        ax1.set_xlabel('Freq (Hz)')
        ax1.set_ylabel('dB')

        ax1.set_ylim([0, MAX_DB])
        ax1.set_xlim(freq_range)

        ax1.grid(True)

        ax2.cla()
        x = np.array(freq)
        y = np.arange(len(waterfall))
        x, y = np.meshgrid(x, y)
        z = np.array(waterfall)

        ax2.plot_surface(x, y, z, cmap='viridis')
        ax2.set_title('Waterfall 3D View')
        ax2.set_xlabel('Freq (Hz)')
        ax2.set_ylabel('Time')
        ax2.set_zlabel('dB')

        ax2.set_ylim([0, MAX_DB])
        ax2.set_xlim(freq_range)

        plt.draw()

    ax_slider = plt.axes((0.2, 0.01, 0.65, 0.03), facecolor='lightgoldenrodyellow')
    slider = Slider(ax_slider, 'Center Freq', -MAX_FREQ, MAX_FREQ, valinit=center_freq)
    slider.on_changed(update_plot)

    while True:
        data = controller.get_serial_data(256)
        if not data:
            continue

        frequencies, spectrum = perform_fft(data, 1000000)
        waterfall.append(spectrum)
        if len(waterfall) > waterfall_lim:
            waterfall.pop(0)

        update_graphs()

        plt.pause(0.001)

except KeyboardInterrupt:
    print("User interrupt")
finally:
    controller.kill()
