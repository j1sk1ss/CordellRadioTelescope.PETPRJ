from overrides import overrides

from front.windows.components.border import Border
from front.windows.components.options import ActionOptions
from front.windows.components.text import Text
from front.windows.window import Menu, Window


class Credits(Menu):
    @overrides
    def generate(self):

        def wexit(body: ActionOptions):
            body.parent.untie()
            self.parent.generate()

        window = Window(
            [
                Border(0, 0),
                Text('Author: Nikolay Fot | J1sk1ss', 1, 1),
                Text('Special thanks: Gansky Pavel Nikolaevich', 1, 2),
                ActionOptions(1, 6, [
                    "0) Exit"
                ], [
                    "<EXIT>"
                ], [
                    wexit
                ])
            ], self.screen
        )

        window.draw()
        window.take_control()
