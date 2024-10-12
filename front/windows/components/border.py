from overrides import overrides
from windows.components.component import Component


class Border(Component):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)

    @overrides
    def draw(self, screen):
        screen.border()

    @overrides
    def read_input(self, user_input):
        pass
