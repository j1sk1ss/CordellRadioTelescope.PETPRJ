from overrides import overrides
from common.common import serial_ports
from driver.nema17 import Nema17
from driver.stm32f103 import STM32
from front.windows.components.options import ActionOptions
from front.windows.components.text import Text
from front.windows.window import Window, Menu


class XYSetup(Menu):
    @overrides
    def generate(self):
        import front.config

        if isinstance(front.config.nema17_driver, Nema17):
            options = [
                f"0) COM-port <{front.config.nema17_driver.controller.port}>",
                f"1) Rotor power <{front.config.nema17_driver.power} V>",
                f"2) Rotor wheel radius <{front.config.nema17_driver.radius} m>",
                f"3) Antenna wheel radius <{front.config.antenna_radius} m>", "4) Exit"
            ]
        else:
            options = [
                "0) COM-port <None>", "1) Rotor power <0 V>",
                "2) Rotor wheel radius <0.0 m>", "3) Antenna wheel radius <0.0 m>", "4) Exit"
            ]

        descriptions = [
            "The COM port used to communicate with the device. Specify the port number to which the device is conn."
            f"\nEnabled devices: \n{' '.join(str(element) for element in serial_ports())}",
            "The power of motor that connected to your microcontroller. Specify the value in V",
            "Motor wheel that connected to antenna wheel radius in meters.",
            "Antenna wheel for navigation, that's connected to motor wheel radius in meters.",
            "<EXIT>"
        ]

# region [XY win handlers]

        def com(body: ActionOptions, data):
            index = int(data)
            body.options[0] = f"0) COM-port <{serial_ports()[index]}>"

            front.config.stm32_driver = STM32(port=serial_ports()[index])
            front.config.nema17_driver = Nema17(stm32=front.config.stm32_driver)
            self.screen.refresh()

        def power(body: ActionOptions, data):  # TODO: nema17 not init
            front.config.nema17_driver.power = int(data)
            body.options[1] = f"1) Rotor power <{front.config.nema17_driver.power} V>"
            self.screen.refresh()

        def rradius(body: ActionOptions, data):
            front.config.nema17_driver.radius = int(data)
            body.options[2] = f"2) Rotor wheel radius <{front.config.nema17_driver.radius} m>"
            self.screen.refresh()

        def aradius(body: ActionOptions, data):
            front.config.antenna_radius = int(data)
            body.options[3] = f"3) Antenna wheel radius <{front.config.antenna_radius} m>"
            self.screen.refresh()

        def wexit(body: ActionOptions):
            body.parent.untie()
            self.parent.generate()

# endregion

        actions = [com, power, rradius, aradius, wexit]

        window = Window(
            [
                Text('XY setup window', 0, 0),
                ActionOptions(0, 2, options, descriptions, actions)
            ], self.screen
        )
        
        window.draw()
        window.take_control()
