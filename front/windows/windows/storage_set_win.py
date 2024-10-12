import psutil

from overrides import overrides

from front.windows.window import Window, Menu
from front.windows.components.text import Text
from front.windows.components.border import Border
from front.windows.components.options import ActionOptions


class StorageSetup(Menu):
    @overrides
    def generate(self):
        import front.config

        options = [
            f"0) Current disk <{front.config.disk_prefix}>", f"1) Save path <{front.config.save_path}>",
            "2) Exit"
        ]

        descriptions = [
            "Disk, where stored captured data. "
            f"{"\n".join([str(x.mountpoint) for x in psutil.disk_partitions()])}",
            "Save path on selected disk.",
            "<EXIT>"
        ]

        def sel_disk(body: ActionOptions, data):
            index = int(data)
            front.config.disk_prefix = psutil.disk_partitions()[index].mountpoint
            body.options[0] = f"0) Current disk <{front.config.disk_prefix}>"
            self.screen.refresh()

        def sel_path(body: ActionOptions, data):
            front.config.save_path = str(data)
            body.options[1] = f"1) Save path <{str(data)}>"
            self.screen.refresh()

        def wexit(body: ActionOptions):
            body.parent.untie()
            self.parent.generate()

        actions = [sel_disk, sel_path, wexit]

        window = Window(
            [
                Border(0, 0),
                Text('Storage setup window', 0, 0),
                ActionOptions(1, 2, options, descriptions, actions)
            ], self.screen
        )

        window.draw()
        window.take_control()
