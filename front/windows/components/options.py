import curses

from overrides import overrides

from common.common import wrap_text
from front.windows.components.component import Component


class ActionOptions(Component):
    def __init__(self, x: int, y: int, options: list, descriptions: list, actions: list):
        """
            Main option class with actions, input modes and descriptions
        Args:
            x (int): X coordinate
            y (int): Y coordinate
            options (list): List of options
            descriptions (list): List of descriptions of options
            actions (list): List of actions
        """

        super().__init__(x, y)
        self.current_index = 0
        self.options = options
        self.descriptions = descriptions
        self.actions = actions

        self.input_mode = False
        self.input_data = ""
        self.input_win = None

    @overrides
    def draw(self, screen):
        for i, option in enumerate(self.options):
            if i == self.current_index:
                screen.addstr(self.y + i, self.x, option, curses.A_REVERSE)
            else:
                screen.addstr(self.y + i, self.x, option)

        height, width = screen.getmaxyx()
        lines = wrap_text(self.descriptions[self.current_index], width)
        num_lines = len(lines)
        start_y = max(height - num_lines, 0)
        for i, line in enumerate(lines):
            y = start_y + i
            screen.addstr(y, self.x, line)

        if self.input_mode:
            self.draw_input_win()

        screen.refresh()

    def draw_input_win(self):
        height, width = 3, 40
        start_y = self.y + 5
        start_x = self.x + 10
        if self.input_win is None:
            self.input_win = curses.newwin(height, width, start_y, start_x)

        self.input_win.clear()
        self.input_win.border()
        self.input_win.addstr(1, 1, "Input: " + self.input_data)
        self.input_win.refresh()

    @overrides
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
                            self.draw_input_win()

            self.parent.draw()
