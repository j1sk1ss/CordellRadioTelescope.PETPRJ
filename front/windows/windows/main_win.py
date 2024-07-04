from overrides import overrides

from front.windows.components.border import Border
from front.windows.components.options import ActionOptions
from front.windows.components.text import FigletText, Text
from front.windows.window import Window, Menu
from front.windows.windows.credits import Credits
from front.windows.windows.move_win import MoveWin
from front.windows.windows.rtl_set_win import RTLSetup
from front.windows.windows.scenario_win import Scenario
from front.windows.windows.spec_win import Spectrum
from front.windows.windows.summary import SummaryWin
from front.windows.windows.waterfall import Waterfall
from front.windows.windows.xy_set_win import XYSetup


class MainMenu(Menu):
    @overrides
    def generate(self):
        options = [
            "0) RTL-SDR setup", "1) X&Y setup",
            "2) Real-time spectrum", "3) Real-time waterfall",
            "4) Real-time movement", "5) Auto-scenario",
            "6) How to basic", "7) Credits"
        ]

        descriptions = [
            "This window will give interface for setting RTL-SDR COM-port. In different OS COM-ports named different. "
            "You should do this as first step.",
            "XY setup needed when you have navigation system of two or more motors. There you can choose COM-port, "
            "power and other stuff.",
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
        spectrum_window = Spectrum(self, self.screen)
        waterfall_window = Waterfall(self, self.screen)
        movement_window = MoveWin(self, self.screen)
        scenario_window = Scenario(self, self.screen)
        summary_window = SummaryWin(self, self.screen)
        credits_window = Credits(self, self.screen)

        actions = [
            lambda: rtl_setup_window.generate(), lambda: xy_setup_window.generate(),
            lambda: spectrum_window.generate(), lambda: waterfall_window.generate(),
            lambda: movement_window.generate(), lambda: scenario_window.generate(),
            lambda: summary_window.generate(), lambda: credits_window.generate()
        ]

        window = Window([
            Border(0, 0),
            FigletText('CRDL RTS', 'nancyj-improved', 80, 0, 0),
            Text('Cordell Radio-Telescope System | Made by Nikolay Fot (j1sk1ss)\nver.: 0.2a | 27.06.24', 0, 6),
            ActionOptions(1, 9, options, descriptions, actions)
        ], self.screen)
        window.draw()

        window.take_control()
