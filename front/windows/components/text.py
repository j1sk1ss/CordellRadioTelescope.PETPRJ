from overrides import overrides

from front.windows.components.component import Component


class Text(Component):
    def __init__(self, text: str, x: int, y: int):
        super().__init__(x, y)
        self.text = text

    @overrides
    def draw(self, screen):
        screen.addstr(self.y, self.x, self.text)
        screen.refresh()


class FigletText(Component):
    def __init__(self, text: str, font: str, h: int, x: int, y: int):
        super().__init__(x, y)

        self.h = h

        self.text = text
        self.font = font

    @overrides
    def draw(self, screen):
        from pyfiglet import Figlet
        f = Figlet(font=self.font, width=self.h)

        screen.addstr(self.y, self.x, f.renderText(self.text))
        screen.refresh()
