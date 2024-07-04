import pandas as pd
from overrides import overrides

from common.common import frange3, spectro_analyze
from driver.nema17 import Nema17, Direction
from front.windows.components.border import Border
from front.windows.components.options import ActionOptions
from front.windows.components.text import Text
from front.windows.window import Menu, Window


class Scenario(Menu):
    @overrides
    def generate(self):
        def scenario_step(x: float, y: float, resolution: int):
            import front.config

            summary = {
                'powers': [],
                'freq': []
            }

            for i in frange3(200, 1766, front.config.rtl_driver.body.sample_rate / 1e6):
                front.config.rtl_driver.set_central_freq(i * 1e6)
                psd_values, frequencies = spectro_analyze(
                    front.config.rtl_driver.body.sample_rate,
                    float(front.config.rtl_driver.get_central_freq()),
                    resolution
                )

                summary['powers'].extend(psd_values)
                summary['freq'].extend(frequencies)

            pd.DataFrame(summary).to_csv(f'snap_in_{x:.1f}_{y:.1f}.csv', index=False)

        def draw_scenario_info():
            import front.config

            self.screen.clear()
            self.screen.border()

            height, width = self.screen.getmaxyx()
            height, width = height - 1, width - 1
            nema = front.config.nema17_driver

            nema: Nema17
            nema.turn_on()
            nema.disable()

            self.screen.addstr(height // 2, width // 2, "Press <s> for start scenario")
            self.screen.addstr((height // 2) + 1, width // 2, "Set your antenna at 80 azimuth")

            answer = self.screen.getch()
            if answer != -1:
                if answer == ord('s'):
                    y = 80

                    for i in range(80):
                        for j in range(200):
                            self.screen.clear()
                            self.screen.border()

                            progress = float((j / 199) * 100)
                            progress_bar = f"[{'#' * (int(progress) // 5)}" \
                                           f"{'-' * (20 - int(progress) // 5)}] {progress:.1f}%"

                            self.screen.addstr(height - 2, width // 2 - len(progress_bar) // 2, progress_bar)
                            self.screen.addstr(height - 1, width // 2, f'y{i} | x{j}')
                            self.screen.refresh()

                            scenario_step(j * 1.8, y - i, 64)
                            nema.move(1.8, Direction.RIGHT, 25000)

                        self.screen.addstr(height // 2, width // 2, "Press <c> to continue")
                        self.screen.addstr((height // 2) + 1, width // 2, f"Set your antenna at {80 - i} azimuth")
                        self.screen.addstr((height // 2) + 2, width // 2, f"Check antenna start angle")
                        self.screen.refresh()
                else:
                    exit(-1)

        def fast_fss():
            self.looped = True
            self.loop(draw_scenario_info)

        def full_fss():
            self.looped = True
            self.loop(draw_scenario_info)

        def fast_s():
            pass

        def full_s():
            pass

        def wexit(body: ActionOptions):
            body.parent.untie()
            self.parent.generate()

        window = Window([
                Border(0, 0),
                Text('Scenarios', 0, 0),
                ActionOptions(
                    1, 1, [
                        "0) Fast-Full sphere scenario",
                        "1) Full-Full sphere scenario",
                        "2) Fast scenario",
                        "3) Full scenario",
                        "4) Exit"
                    ], [
                        "Will use SatFinder (If it presented) as signal detector. Save only level of signal "
                        "with coordinates.",
                        "Will use RTL2832U (If it presented) as signal detector and spectral analyzer. "
                        "It will take more time for scenario. Also, be sure that you have enough space "
                        "for data.",
                        "<WIP>",
                        "<WIP>",
                        "<EXIT>"
                    ], [
                        fast_fss, full_fss, fast_s, full_s, wexit
                    ]
                )
            ], self.screen
        )

        window.draw()
        window.take_control()
