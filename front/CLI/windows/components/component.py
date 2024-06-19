class Component:
    def __init__(self, x, y, screen, parent=None):
        self.screen = screen
        self.x = x
        self.y = y
        self.parent = parent
    
    def draw(self):
        pass
    