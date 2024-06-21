import serial

from common.common import serial_ports
from driver.stm32f103 import STM32
from front.CLI.windows.components.options import ActionOptions
from front.CLI.windows.window import Window


def generate():
    import front.CLI.cli_ver

    options = [
        f"0) COM-port <{front.CLI.cli_ver.rotor_com_port}>", f"1) Rotor power <{front.CLI.cli_ver.rotor_power} V>",
        f"2) Rotor wheel radius <{front.CLI.cli_ver.rotor_radius} m>",
        f"3) Antenna wheel radius <{front.CLI.cli_ver.antenna_radius} m>", "4) Exit"
    ]

    descriptions = [
        "The COM port used to communicate with the device. Specify the port number to which the device is connected."
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

        front.CLI.cli_ver.rtl_driver = STM32(port=serial_ports()[index])
        front.CLI.cli_ver.main_screen.refresh()

    def power(body: ActionOptions, data):
        front.CLI.cli_ver.rotor_power = int(data)
        body.options[1] = f"1) Rotor power <{front.CLI.cli_ver.rotor_power} V>"
        front.CLI.cli_ver.main_screen.refresh()

    def rradius(body: ActionOptions, data):
        front.CLI.cli_ver.rotor_radius = int(data)
        body.options[2] = f"2) Rotor wheel radius <{front.CLI.cli_ver.rotor_radius} m>"
        front.CLI.cli_ver.main_screen.refresh()

    def aradius(body: ActionOptions, data):
        front.CLI.cli_ver.antenna_radius = int(data)
        body.options[3] = f"3) Antenna wheel radius <{front.CLI.cli_ver.antenna_radius} m>"
        front.CLI.cli_ver.main_screen.refresh()

    def wexit(body: ActionOptions):
        body.parent.untie()
        front.CLI.cli_ver.main_window()

    # endregion

    actions = [com, power, rradius, aradius, wexit]

    window = Window(
        [
            ActionOptions(1, 2, options, descriptions, actions, front.CLI.cli_ver.main_screen)
        ], front.CLI.cli_ver.main_screen
    )
    window.draw()

    window.take_control()
