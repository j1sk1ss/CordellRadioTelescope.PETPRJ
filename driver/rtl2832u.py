from overrides import overrides
from rtlsdr import RtlSdr

from driver.driver import Driver


class RTL(Driver):
    def __init__(self, serial):
        self.body = RtlSdr(serial_number=serial)
        self.serial = serial

        self.sample_count = 512
        self.update_delay = 0.05

    def set_sample_rate(self, rate):
        self.body.set_sample_rate(rate)

    def get_sample_rate(self):
        return self.body.get_sample_rate()

    def set_central_freq(self, freq):
        self.body.set_center_freq(freq)

    def change_central_freq(self, freq):
        self.set_central_freq(self.get_central_freq() + freq)

    def get_central_freq(self):
        return self.body.get_center_freq()

    def set_gain(self, gain):
        self.body.gain = gain

    def set_sample_count(self, samples):
        self.sample_count = samples

    @overrides
    def read(self, count):
        return self.get_samples()

    def get_samples(self):
        return self.body.read_samples(self.sample_count)

    @overrides
    def kill(self):
        self.body.close()

    @staticmethod
    def get_serials():
        return RtlSdr.get_device_serial_addresses()
