from overrides import overrides
from rtlsdr import RtlSdr

from driver.driver import Driver


class RTL(Driver):
    def __init__(self, serial):
        self.body = RtlSdr(serial_number=serial)
        self.sample_count = 512

    def set_sample_rate(self, rate):
        self.body.sample_rate = rate

    def set_central_freq(self, freq):
        self.body.center_freq = freq

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
