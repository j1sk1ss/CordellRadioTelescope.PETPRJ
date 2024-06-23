from driver.driver import Driver
from driver.stm32f103 import STM32
from enum import Enum


class Commands(Enum):
    START = 's'
    STOP = 'k'

    @staticmethod
    def right(speed):
        return f'f{speed}'

    @staticmethod
    def left(speed):
        return f'b{speed}'


class Direction(Enum):
    RIGHT = 0
    LEFT = 1
    NONE = -1


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

        # More = slower
        self.speed = 0

    def change_direction(self, direction: Direction):
        """
        Change direction of Nema17
        :param direction: Direction of moving
        """

        if direction is Direction.RIGHT:
            self.controller.send(Commands.right(self.speed))
        elif direction is Direction.LEFT:
            self.controller.send(Commands.left(self.speed))
        elif direction is Direction.NONE:
            self.controller.send(Commands.STOP)

    def change_speed(self, speed: int):
        """
        Change speed of Nema17
        :param speed: Speed of moving
        """

        if self.direction is Direction.RIGHT:
            self.controller.send(Commands.right(speed))
        elif self.direction is Direction.LEFT:
            self.controller.send(Commands.left(speed))
        elif self.direction is Direction.NONE:
            self.controller.send(Commands.STOP)

    def enable(self):
        self.controller.send(Commands.START)

    def disable(self):
        self.controller.send(Commands.STOP)
