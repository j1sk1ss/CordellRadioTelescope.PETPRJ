import curses


class Window:
    def __init__(self, components: list, screen):
        self.components = components
        for component in components:
            component.parent = self
        
        self.screen = screen
        self.lock_component = None
        
        self.is_control = False
    
    def lock(self, index):
        self.lock_component = self.components[index]
    
    def read_input(self, user_input):
        if self.lock_component != None:
            self.lock_component.read_input(user_input)
        else:
            for component in self.components:
                component.read_input(user_input)
    
    def draw(self):
        curses.curs_set(0)
        self.screen.clear()
        
        for component in self.components:
            component.draw()
            
    def take_control(self):
        self.is_control = True
        while self.is_control:
            key = self.screen.getch()
            self.read_input(key)
    
    def untie(self):
        self.is_control = False
    