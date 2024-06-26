from overrides import overrides
from driver.rtl2832u import RTL
from front.windows.components.options import ActionOptions
from front.windows.components.text import Text
from front.windows.window import Window, Menu


class RTLSetup(Menu):
    @overrides
    def generate(self):
        import front.config

        if isinstance(front.config.rtl_driver, RTL):
            options = [
                f"0) COM-port <{front.config.rtl_driver.serial}>",
                f"1) Center frequency <{front.config.rtl_driver.body.center_freq / 10e6} mHz>",
                f"2) Sample rate <{front.config.rtl_driver.body.sample_rate / 10e6} mHz>",
                f"3) Tuner gain mode <{front.config.rtl_driver.body.gain}>",
                f"4) Sample count <{front.config.rtl_driver.sample_count}>",
                f"5) Update delay <{front.config.rtl_driver.update_delay} s>", "6) Exit"
            ]
        else:
            options = [
                "0) COM-port <None>", "1) Center frequency <0.0 mHz>",
                "2) Sample rate <2.048 mHz>", "3) Tuner gain mode <auto>",
                "4) Sample count <512>", "5) Update delay <0.1 s>", "6) Exit"
            ]

        descriptions = [
            "The COM port used to communicate with the device. Specify the port number to which the device is conn."
            f"\nEnabled devices: \n{' '.join(str(element) for element in RTL.get_serials())}",
            "The center frequency that the receiver is tuned to. Specify the value in MHz.",
            "The sampling rate for capturing signals. Specify the value in MHz.",
            "The tuner gain mode. Choose the mode that controls the gain level for signal reception.",
            "Count of samples", "Update delay in spectrum and waterfall. Lower - higher update rate",
            "<EXIT>"
        ]

        # region [RTL win handlers]

        def com(body: ActionOptions, data):
            index = int(data)
            body.options[0] = f"0) COM-port <index: {index} ({RTL.get_serials()[index]})>"

            front.config.rtl_driver = RTL(RTL.get_serials()[index])
            front.config.rtl_driver.set_sample_count(512)
            front.config.rtl_driver.set_gain('auto')
            front.config.rtl_driver.set_sample_rate(2.048e6)

            self.screen.refresh()

        def cfreq(body: ActionOptions, data):
            freq = int(data)
            body.options[1] = f"1) Center frequency <{freq} mHz>"
            front.config.rtl_driver.set_central_freq(freq * 10e6)
            self.screen.refresh()

        def srate(body: ActionOptions, data):
            rate = int(data)
            body.options[2] = f"2) Sample rate <{rate} mHz>"
            front.config.rtl_driver.set_sample_rate(rate * 10e6)
            self.screen.refresh()

        def tuner(body: ActionOptions, data):
            gain = data
            body.options[3] = f"3) Tuner gain mode <{gain}>"
            front.config.rtl_driver.set_gain(gain)
            self.screen.refresh()

        def scount(body: ActionOptions, data):
            count = int(data)
            body.options[4] = f"4) Sample count <{count}>"
            front.config.rtl_driver.set_sample_count(count)
            self.screen.refresh()

        def udelay(body: ActionOptions, data):
            front.config.rtl_driver.update_delay = float(data)
            body.options[5] = f"5) Update delay <{front.config.rtl_driver.update_delay} s>"
            self.screen.refresh()

        def wexit(body: ActionOptions):
            body.parent.untie()
            self.parent.generate()

        # endregion

        window = Window([
            Text('RTL setup window', 0, 0),
            ActionOptions(0, 2, options, descriptions,
                          [com, cfreq, srate, tuner, scount, udelay, wexit]
                          )
        ], self.screen)

        window.draw()
        window.take_control()
