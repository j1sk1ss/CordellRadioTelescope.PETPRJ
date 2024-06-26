from overrides import overrides

from front.windows.components.border import Border
from front.windows.components.controller import BoxKeyHandler
from front.windows.components.text import Text
from front.windows.window import Menu, Window


# region [Tips]

tips = [
    'The first thing to do is to determine your budget. In theory, you can do with much less money, '
    'if you do not pretend to analyze the data in depth, and stop at the usual scanning with obtaining '
    'the signal level. For such people who do not need deep analysis, special clarifications will be added '
    'to the main text. Anyway, here we go.',
    'For the radio telescope will need to buy or find a direct-focus satellite TV dish, with a diameter '
    'of at least a meter. It is desirable with a receiver in the range from 4 to 6 GHz, not in the Ku range '
    'to in modern dishes. Also stock up on kao-axial cable, TV splitters and adapters from SMA to F. '
    '(If you have the second option, you can take not only a direct-focus dish. '
    'You can take an offset with a much smaller diameter. A Ku-band receiver is also suitable)',
    'Now lets talk about nutrition. Feeding the plate, more often than not, is essential. '
    'This is due to the fact that the antenna is active.  Power can be organized through a TV splitter with a '
    'power pass, where at one end of the dish, at the first output of the battery at 12 + volts, and at the second '
    'output of the receiver signal (splitter is necessary in order not to burn the receiver and not to shunt '
    'the signal) (For people with the second option, you can limit yourself without using a TV splitter. '
    'You need to buy a SatFinder, put it between the power supply and the dish, and after receiving the '
    'signal from there, process it with a microcontroller. The code and detailed analysis can be found on YouTube)',
    'Next, the received signal should be sent to RTL2832U or similar. You can use this software as well as SDRSharp, '
    'CubicSDR and so on. (Those who chose the second option do not need this software. They are needed for spectral '
    'analysis of the received signals)'
]

# endregion


current_tip = 0


class SummaryWin(Menu):
    @overrides
    def generate(self):

        height, width = self.screen.getmaxyx()
        height, width = height - 1, width - 1

# region [Tip handlers]

        def next_tip(body: BoxKeyHandler, components: list):
            global current_tip
            if current_tip < len(tips) - 1:
                current_tip += 1

            body = components[0]
            body.text = tips[current_tip]
            self.screen.refresh()

        def previous_tip(body: BoxKeyHandler, components: list):
            global current_tip
            if current_tip > 0:
                current_tip -= 1

            body = components[0]
            body.text = tips[current_tip]
            self.screen.refresh()

        def wexit(body: BoxKeyHandler, components: list):
            body.parent.untie()
            self.parent.generate()

# endregion

        global current_tip
        current_tip = 0

        info_text = Text(tips[current_tip], 1, 1)
        window = Window([
            Border(0, 0),
            BoxKeyHandler(0, 0, [
                info_text
            ], 67, next_tip),  # Next
            BoxKeyHandler(0, 0, [
                info_text
            ], 68, previous_tip),  # Previous
            BoxKeyHandler(0, 0, [
            ], ord('q'), wexit),  # Previous
            Text('<- Previous | q - exit | Next ->', 0, height)
        ], self.screen)

        window.draw()
        window.take_control()
