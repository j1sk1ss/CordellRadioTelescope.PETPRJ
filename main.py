import flet as ft
import pandas as pd
from flet.plotly_chart import PlotlyChart
import plotly.express as px

from common.common import perform_fft
from driver.stm32.stm32 import STM32


# region [Serial]

frequencies = [0]
spectrum = [0]
controller = STM32()

# endregion

# region [Graphs]

SPECTRAL_START = 0
SPECTRAL_END = 1000

serial_data = controller.get_serial_data(1024)
freq, db = perform_fft(serial_data, 1000000)

spectral_data = {
    'freq': freq,
    'dB': db
}

spectrum_frame = PlotlyChart(
    px.line(
        pd.DataFrame(spectral_data), x='freq', y='dB'
    ), expand=True
)

# endregion


def update_data():
    incoming_data = controller.get_serial_data(1024)

    global frequencies, spectrum
    frequencies, spectrum = perform_fft(incoming_data, 1000000)


def main(page: ft.Page):
    page.title = 'Cordell RSA'
    page.theme_mode = 'light'
    page.vertical_alignment = ft.MainAxisAlignment.START

    page.window_width = 800
    page.window_height = 800
    page.window_resizable = False

    page.add(ft.Row([spectrum_frame]))

    def update_chart():
        while True:
            update_data()

            global spectral_data
            spectral_data = {
                'freq': frequencies[int(SPECTRAL_START):int(SPECTRAL_END)],
                'dB': spectrum[int(SPECTRAL_START):int(SPECTRAL_END)]
            }

            print(SPECTRAL_END)

            spectrum_frame.figure = px.line(pd.DataFrame(spectral_data), x='freq', y='dB')
            spectrum_frame.update()

            page.update()

    def change_center(e):
        global SPECTRAL_START
        SPECTRAL_START = 0 + e.control.value

        global SPECTRAL_END
        SPECTRAL_END = 1000 + e.control.value

    page.add(ft.Row([ft.Slider(
        min=-4000,
        max=4000,
        value=0,
        divisions=100,
        on_change=change_center)]
    ))

    page.update()

    update_chart()


ft.app(target=main)
