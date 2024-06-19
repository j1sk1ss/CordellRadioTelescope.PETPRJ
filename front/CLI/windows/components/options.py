

import curses

from front.CLI.windows.components.component import Component


class Options(Component):
    def __init__(self, x: int, y: int, options: list, descriptions: list, screen):
        """
            This component represent menu of menu items (strings) with descriptions
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            options (list): List of options in menu
            descriptions (list): List of option descriptions
            screen (_type_): Main screen
        """
        
        super().__init__(x, y, screen)
        
        self.current_index = 0
        self.options       = options
        self.descriptions  = descriptions
        
    def draw(self):
        self.screen.clear()
        for i, option in enumerate(self.options):
            if i == self.current_index:
                self.screen.addstr(self.y + i, self.x, option, curses.A_REVERSE)
            else:
                self.screen.addstr(self.y + i, self.x, option)
        
        self.screen.addstr(self.y + len(self.options) + 1, self.x, self.descriptions[self.current_index])
        self.screen.refresh()
    
    def read_input(self, user_input):
        if user_input == curses.KEY_UP:
            self.current_index = (self.current_index - 1) % len(self.options)
        elif user_input == curses.KEY_DOWN:
            self.current_index = (self.current_index + 1) % len(self.options)
            
        self.draw()
    
    
class ActionOptions(Component):
    def __init__(self, x: int, y: int, options: list, descriptions: list, actions: list, screen):
        """
            Main option class with actions, input modes and descriptions
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            options (list): List of options
            descriptions (list): List of descriptions of options
            actions (list): List of actions
            screen (_type_): Curses main screen
            input_mode (bool): False - default, True - with input appereance
        """
        
        super().__init__(x, y, screen)
        self.current_index = 0
        self.options       = options
        self.descriptions  = descriptions
        self.actions       = actions
        
        self.input_mode = False
        self.input_data = ""
        self.input_win  = None
        
    def draw(self):
        self.screen.clear()
        for i, option in enumerate(self.options):
            if i == self.current_index:
                self.screen.addstr(self.y + i, self.x, option, curses.A_REVERSE)
            else:
                self.screen.addstr(self.y + i, self.x, option)
                
        self.screen.addstr(self.y + len(self.options) + 1, self.x, self.descriptions[self.current_index])
        
        if self.input_mode:
            self.draw_input_win()
            
        self.screen.refresh()
    
    def draw_input_win(self):
        height, width = 3, 40
        start_y = self.y + 5
        start_x = self.x + 5
        if self.input_win is None:
            self.input_win = curses.newwin(height, width, start_y, start_x)
            
        self.input_win.clear()
        self.input_win.border()
        self.input_win.addstr(1, 1, "Data: " + self.input_data)
        self.input_win.refresh()
    
    def read_input(self, user_input):
        def close():
            self.input_mode = False
            self.input_data = ""
            self.input_win.clear()
            self.input_win.refresh()
            self.input_win = None            
        
        if self.input_mode:
            if user_input == 10:  # ENTER
                self.actions[self.current_index](self, self.input_data)
                close()
            elif user_input == 27:  # ESC
                close()
            elif user_input == curses.KEY_BACKSPACE or user_input == 127:
                self.input_data = self.input_data[:-1]
            elif user_input != curses.KEY_RESIZE:
                self.input_data += chr(user_input)
                
            self.draw_input_win()
        else:
            if user_input == (27 and 91 and 65):
                self.current_index = (self.current_index - 1) % len(self.options)
            elif user_input == (27 and 91 and 66):
                self.current_index = (self.current_index + 1) % len(self.options)
            elif user_input == 10:  # ENTER
                if self.actions[self.current_index] is not None:
                    if callable(self.actions[self.current_index]):
                        if self.actions[self.current_index].__code__.co_argcount == 0:
                            self.actions[self.current_index]()
                        elif self.actions[self.current_index].__code__.co_argcount == 1:
                            self.actions[self.current_index](self)
                        elif self.actions[self.current_index].__code__.co_argcount == 2:
                            self.input_mode = True
                        
            self.draw()
    