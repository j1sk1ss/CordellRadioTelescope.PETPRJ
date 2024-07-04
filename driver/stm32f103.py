import time

import serial

from overrides import overrides
from driver.driver import Driver


class STM32(Driver):
    def __init__(self, port='COM4', bound_rate=9600):
        try:
            self.port = port
            self.serial = serial.Serial(port, bound_rate, timeout=1)
        except Exception as e:
            print(f"Serial error: {e}")
            exit()

    @overrides
    def read(self, count) -> list:
        """
        :param count: Count of bytes to read
        :return: Data read from serial port
        """
        samples = []
        while len(samples) < count:
            try:
                line = self.serial.readline()
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

#    @overrides
    def send(self, data: str):
        """
        :param data: Data write to serial port
        """
        self.serial.write(data.encode())

    @overrides
    def kill(self):
        """
        Kill serial connection
        """
        self.serial.close()
        print("Serial connection closed")
