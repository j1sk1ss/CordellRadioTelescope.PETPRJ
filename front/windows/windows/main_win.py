from overrides import overrides

from windows.components.border import Border
from windows.components.text import FigletText, Text
from windows.components.options import ActionOptions

from windows.window import Window, Menu
from windows.windows.credits import Credits
from windows.windows.move_win import MoveWin
from windows.windows.spec_win import Spectrum
from windows.windows.xy_set_win import XYSetup
from windows.windows.summary import SummaryWin
from windows.windows.waterfall import Waterfall
from windows.windows.rtl_set_win import RTLSetup
from windows.windows.scenario_win import Scenario
from windows.windows.storage_set_win import StorageSetup


class MainMenu(Menu):
    @overrides
    def generate(self):
        options = [
            "0) RTL-SDR setup", "1) X&Y setup", "2) Storage setup",
            "3) Real-time spectrum", "4) Real-time waterfall",
            "5) Real-time movement", "6) Auto-scenario",
            "7) How to basic", "8) Credits"
        ]

        descriptions = [
            "This window will give interface for setting RTL-SDR COM-port. In different OS COM-ports named different. "
            "You should do this as first step.",
            "XY setup needed when you have navigation system of two or more motors. There you can choose COM-port, "
            "power and other stuff.",
            "Set storage folder on disk / external disk for saving collected data",
            "Spectrum analyzer window show spectrum in real time. RTL-SDR send data by serial port to Cordell RSA, "
            "then Cordell RSA draw graphs of spectrum.",
            "Waterfall window is a second part of spectrum window. Every second this window draws line of spectrum, "
            "store, and move it down. With this window you can find blinking signal.",
            "XY movement window for working with your navigation system. Don`t forget check XY setup window.",
            "Auto-scenario is algorithms for auto data analyze and auto data preparing.",
            "Summary window includes data about authors and simple guide how to create your own radio-telescope",
            "<CREDITS>"
        ]

        rtl_setup_window = RTLSetup(self, self.screen)
        xy_setup_window = XYSetup(self, self.screen)
        storage_setup_window = StorageSetup(self, self.screen)
        spectrum_window = Spectrum(self, self.screen)
        waterfall_window = Waterfall(self, self.screen)
        movement_window = MoveWin(self, self.screen)
        scenario_window = Scenario(self, self.screen)
        summary_window = SummaryWin(self, self.screen)
        credits_window = Credits(self, self.screen)

        actions = [
            lambda: rtl_setup_window.generate(), lambda: xy_setup_window.generate(),
            lambda: storage_setup_window.generate(), lambda: spectrum_window.generate(),
            lambda: waterfall_window.generate(), lambda: movement_window.generate(),
            lambda: scenario_window.generate(), lambda: summary_window.generate(),
            lambda: credits_window.generate()
        ]

        window = Window([
            Border(0, 0),
            FigletText('CRDL RTS', 'nancyj-improved', 80, 0, 0),
            Text('Cordell Radio-Telescope System | Made by Nikolay Fot (j1sk1ss)\nver.: 0.2b | 12.10.24', 0, 6),
            ActionOptions(1, 9, options, descriptions, actions)
        ], self.screen)
        window.draw()

        window.take_control()
