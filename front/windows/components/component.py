class Component:
    def __init__(self, x: int, y: int, parent=None):
        self.x = x
        self.y = y
        self.parent = parent

    def read_input(self, user_input):
        pass

    def draw(self, screen):
        pass
    