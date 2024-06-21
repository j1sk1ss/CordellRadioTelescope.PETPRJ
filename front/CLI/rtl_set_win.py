from driver.rtl2832u import RTL
from front.CLI.windows.components.options import ActionOptions
from front.CLI.windows.window import Window


def generate():
    import front.CLI.cli_ver

    options = [
        f"0) COM-port <{front.CLI.cli_ver.rtl_com_port}>", f"1) Center frequency <{front.CLI.cli_ver.central_freq} mHz>", f"2) Sample rate <{front.CLI.cli_ver.sample_rate} mHz>",
        f"3) Tuner gain mode <{front.CLI.cli_ver.tuner_gain}>", f"4) Sample count <{front.CLI.cli_ver.sample_count}>", "5) Exit"
    ]

    descriptions = [
        "The COM port used to communicate with the device. Specify the port number to which the device is connected."
        f"\nEnabled devices: \n{' '.join(str(element) for element in RTL.get_serials())}",
        "The center frequency that the receiver is tuned to. Specify the value in MHz.",
        "The sampling rate for capturing signals. Specify the value in MHz.",
        "The tuner gain mode. Choose the mode that controls the gain level for signal reception.",
        "Count of samples",
        "<EXIT>"
    ]

    # region [RTL win handlers]

    def com(body: ActionOptions, data):
        index = int(data)
        body.options[0] = f"0) COM-port <index: {index} ({RTL.get_serials()[index]})>"

        front.CLI.cli_ver.rtl_driver = RTL(RTL.get_serials()[index])
        front.CLI.cli_ver.rtl_driver.set_sample_count(512)
        front.CLI.cli_ver.rtl_driver.set_gain('auto')
        front.CLI.cli_ver.rtl_driver.set_sample_rate(2.048e6)

        front.CLI.cli_ver.main_screen.refresh()

    def cfreq(body: ActionOptions, data):
        front.CLI.cli_ver.central_freq = int(data)
        body.options[1] = f"1) Center frequency <{front.CLI.cli_ver.central_freq} mHz>"

        front.CLI.cli_ver.rtl_driver.set_central_freq(front.CLI.cli_ver.central_freq * 10e6)

        front.CLI.cli_ver.main_screen.refresh()

    def srate(body: ActionOptions, data):
        front.CLI.cli_ver.sample_rate = int(data)
        body.options[2] = f"2) Sample rate <{front.CLI.cli_ver.sample_rate} mHz>"

        front.CLI.cli_ver.rtl_driver.set_sample_rate(front.CLI.cli_ver.sample_rate * 10e6)

        front.CLI.cli_ver.main_screen.refresh()

    def tuner(body: ActionOptions, data):
        front.CLI.cli_ver.tuner_gain = data
        body.options[3] = f"3) Tuner gain mode <{front.CLI.cli_ver.tuner_gain}>"

        front.CLI.cli_ver.rtl_driver.set_gain(front.CLI.cli_ver.tuner_gain)

        front.CLI.cli_ver.main_screen.refresh()

    def scount(body: ActionOptions, data):
        front.CLI.cli_ver.sample_count = int(data)
        body.options[4] = f"4) Sample count <{front.CLI.cli_ver.sample_count}>"

        front.CLI.cli_ver.rtl_driver.set_sample_count(front.CLI.cli_ver.sample_count)

        front.CLI.cli_ver.main_screen.refresh()

    def wexit(body: ActionOptions):
        body.parent.untie()
        front.CLI.cli_ver.main_window()

    # endregion

    actions = [com, cfreq, srate, tuner, scount, wexit]

    window = Window([ActionOptions(1, 2, options, descriptions, actions, front.CLI.cli_ver.main_screen)], front.CLI.cli_ver.main_screen)
    window.draw()

    window.take_control()
