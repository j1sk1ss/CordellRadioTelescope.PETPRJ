using Colorify;
using Colorify.UI;
using Figgle;


namespace CordellRadioTelescope.EXMPL.window {
    public class ProgramWindow {
        public ProgramWindow(ConsoleColor backGround, Format colorFormat) {
            _backGround  = backGround;
            _colorFormat = colorFormat;

            _colorFormat.ResetColor();
            _colorFormat.Clear();

            ClearScreen(backGround);
        }

        private ConsoleColor _backGround { get; set; } 
        private Format _colorFormat { get; set; }

        public void DrawMainWindow() {

            // Info data

            var _option = "0) RTL-SDR setup";

            var _options = new List<string> {
                "0) RTL-SDR setup", "1) XY setup", "2) Spectrum", "3) Waterfall", "4) Movement", "5) Summary"
            };

            var _descriptions = new List<string> {
                "This window will give interface for setting RTL-SDR COM-port. In different OS COM-ports named differend. You should do this as first step.",
                "XY setup needed when you have navigation system of two or more motors. There you can choose COM-port, power and other stuff.",
                "Spectrum analyzer window show spectrum in real time. RTL-SDR send data by serial port to Cordell RSA, then Cordell RSA draw graphs of spectrum.",
                "Waterfall window is a second part of spectrum window. Every second whis window draws line of spectrum, store, and move it down. With this window you can find blinking sighnal.",
                "XY movement window for working with your navigation system. Don`t forget check XY setup window.", 
                "Summary window includes data about authors and simple guide how to create your own radiotelescope"
            };

            var _windowActions = new List<Action> {
                DrawRTLsetupWindow, DrawXYsetupWindow, DrawSpectrumWindow, DrawWaterfallWindow, DrawMovementWindow, DrawSummaryWindow
            };

            // Window loop

            while (true) {
                _colorFormat.AlignCenter("Cordell RSA program. Credits: j1sk1ss", Colors.bgSuccess);

                Console.WriteLine(FiggleFonts.Standard.Render("Cordell RSA"));
                Console.WriteLine("\n\n\n\n\n\n");

                foreach (var option in _options) {
                    if (option == _option) _colorFormat.WriteLine(option, Colors.bgWarning);
                    else _colorFormat.WriteLine(option, Colors.bgMuted);
                }

                Console.WriteLine("\n\n\n");
                _colorFormat.DivisionLine('-', Colors.bgDefault);
                Console.WriteLine(_descriptions[_options.IndexOf(_option)]);

                var answer = Console.ReadKey(false).Key;
                if (answer == ConsoleKey.UpArrow) _option = _options[Math.Max(_options.IndexOf(_option) - 1, 0)];
                else if (answer == ConsoleKey.DownArrow) _option = _options[Math.Min(_options.IndexOf(_option) + 1, _options.Count - 1)];
                else {
                    break;
                }

                ClearScreen(ConsoleColor.White);
            }
        }

        private void DrawRTLsetupWindow() {

        }

        private void DrawXYsetupWindow() {

        }

        private void DrawSpectrumWindow() {

        }

        private void DrawWaterfallWindow() {

        }

        private void DrawMovementWindow() {

        }

        private void DrawSummaryWindow() {

        }

        private void ClearScreen(ConsoleColor color) {
            Console.BackgroundColor = color;
            Console.SetCursorPosition(0, 0);
            Console.Clear();
        }
    }
}
