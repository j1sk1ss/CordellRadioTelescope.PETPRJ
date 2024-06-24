import time

import serial

from overrides import overrides
from driver.driver import Driver


class STM32(Driver):
    def __init__(self, port='COM4', bound_rate=115200):
        try:
            self.port = port
            self.serial = serial.Serial(port, bound_rate, timeout=1)
        except Exception as e:
            print(f"Serial error: {e}")
            exit()

    @overrides
    def read(self, count):
        """
        :param count: Count of bytes to read
        :return: Data read from serial port
        """
        samples = []
        while len(samples) < count:
            try:
                line = self.readline_with_timeout(10)
                if line:
                    samples.append(int(line))
            except Exception as exp:
                print(f"Data error: {exp}")
                break

        return samples

    def readline_with_timeout(self, timeout=1):
        start_time = time.time()
        line = bytearray()
        while True:
            if self.serial.inWaiting() > 0:
                char = self.serial.read(1)
                if char == b'\n':
                    break

                line.extend(char)

            if time.time() - start_time > timeout:
                break

        return line.decode('utf-8').strip()

    @overrides
    def send(self, data):
        """
        :param data: Data write to serial port
        """
        for part in data:
            self.serial.write(part.encode('utf-8'))

    @overrides
    def kill(self):
        """
        Kill serial connection
        """
        self.serial.close()
        print("Serial connection closed")
