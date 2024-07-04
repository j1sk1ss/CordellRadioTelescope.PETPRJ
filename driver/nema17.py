import time
from typing import overload

from driver.driver import Driver
from driver.stm32f103 import STM32
from enum import Enum


class Direction(Enum):
    RIGHT = 'f'
    LEFT = 'b'
    NONE = 'n'


class Commands(Enum):
    START = 's'
    STOP = 'k'
    ENABLE = 'e'
    DISABLE = 'd'

    @staticmethod
    def right(speed):
        return f'{Direction.RIGHT}{speed}'

    @staticmethod
    def left(speed):
        return f'{Direction.LEFT}{speed}'

    @staticmethod
    def none(speed):
        return f'{Direction.NONE}{speed}'

    @staticmethod
    def move(direction: Direction, speed: int, steps: float):
        return f'{direction.value}{speed}s{int(steps)}'


class Nema17(Driver):
    """
    Nema17 driver for Cordell RSA
    """

    def __init__(self, stm32: STM32):
        """
        Init of Nema17
        :param stm32: STM32 driver
        """

        self.controller = stm32
        self.direction = Direction.NONE
        self.steps_per_degree = 1.8

        self.power = 0
        self.radius = 0

        # More = slower
        self.speed = 0

    def is_connected(self):
        """
        Check Nema17 connection status
        :return: Connection status
        """
        time.sleep(0.25)
        self.controller.send('!')

        try_count = 1000
        answer = 'not connected'
        while try_count > 0 and answer != 'connected':
            answer = self.controller.read(1)
            try_count -= 1

        return answer == 'connected'

    def change_direction(self, direction: Direction):
        """
        Change direction of Nema17
        :param direction: Direction of moving
        """

        time.sleep(0.25)
        if direction is Direction.RIGHT:
            self.controller.send(Commands.right(self.speed))
        elif direction is Direction.LEFT:
            self.controller.send(Commands.left(self.speed))
        elif direction is Direction.NONE:
            self.controller.send(Commands.DISABLE.value)

    def change_speed(self, speed: int):
        """
        Change speed of Nema17
        :param speed: Speed of moving
        """
        time.sleep(0.25)
        self.controller.send(Commands.none(speed))

    @overload
    def move(self, degrees: float):
        ...

    @overload
    def move(self, degrees: float, direction: Direction, speed: int):
        ...

    def move(self, *args):
        time.sleep(1)
        if len(args) == 1:
            degrees = float(args[0])
            self.controller.send(Commands.move(self.direction, self.speed, degrees / self.steps_per_degree))
        elif len(args) == 3:
            degrees = float(args[0])
            direction = args[1]
            speed = int(args[2])
            self.controller.send(Commands.move(direction, speed, degrees / self.steps_per_degree))

    def turn_on(self):
        """
        Turn ON nema17 drv8825
        """
        time.sleep(1.25)
        self.controller.send(Commands.START.value)

    def enable(self):
        """
        Enable Nema17 infinity movement
        """
        time.sleep(1.25)
        self.controller.send(Commands.ENABLE.value)

    def turn_off(self):
        """
        Turn OFF nema17 drv8825
        """
        time.sleep(1.25)
        self.controller.send(Commands.STOP.value)

    def disable(self):
        """
        Disable Nema17 infinity movement
        """
        time.sleep(1.25)
        self.controller.send(Commands.DISABLE.value)
