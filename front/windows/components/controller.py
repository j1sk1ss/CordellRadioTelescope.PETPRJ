from overrides import overrides

from front.windows.components.component import Component


class BoxKeyHandler(Component):
    def __init__(self, x: int, y: int, components: list, key, action):
        super().__init__(x, y)

        self.components = components
        self.key = key
        self.action = action

    @overrides
    def draw(self, screen):
        for i in self.components:
            i.draw(screen)

    @overrides
    def read_input(self, user_input):
        if user_input == self.key:
            self.action(self, self.components)
            self.parent.draw()
