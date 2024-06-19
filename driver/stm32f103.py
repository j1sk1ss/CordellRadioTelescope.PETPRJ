import serial


class STM32:
    def __init__(self, port='COM4', bound_rate=115200):
        try:
            self.serial = serial.Serial(port, bound_rate, timeout=1)
        except Exception as e:
            print(f"Serial error: {e}")
            exit()

    def get_serial_data(self, count):
        """
        :param count: Count of bytes to read
        :return: Data read from serial port
        """
        samples = []
        while len(samples) < count:
            try:
                line = self.serial.readline().decode('utf-8').strip()
                if line:
                    samples.append(int(line))
            except Exception as exp:
                print(f"Data error: {exp}")
                break

        return samples

    def send_serial_data(self, data):
        """
        :param data: Data write to serial port
        """
        for part in data:
            self.serial.write(part.encode('utf-8'))

    def kill(self):
        """
        Kill serial connection
        """
        self.serial.close()
        print("Serial connection closed")
