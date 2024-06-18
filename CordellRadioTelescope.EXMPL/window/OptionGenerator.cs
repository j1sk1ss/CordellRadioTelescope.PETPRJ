using Colorify;
using Figgle;


namespace CordellRadioTelescope.EXMPL.window {
    public class OptionGenerator {
        public OptionGenerator(List<string> options) {
            _options = options;
            _option  = _options[0];

            _descriptions = null;
            _actions      = null;
        }

        public OptionGenerator(List<string> options, List<string> descriptions, List<Action> actions) {
            _options = options;
            _option  = _options[0];

            _descriptions = descriptions;
            _actions      = actions;
        }

        private string _option {  get; set; }
        private List<string> _options {  get; set; }
        private List<string>? _descriptions { get; set; }
        private List<Action>? _actions { get; set; }
        
        public void DrawOptions(Format _colorFormat) {
            foreach (var option in _options) {
                if (option == _option) _colorFormat.WriteLine(option, Colors.bgWarning);
                else _colorFormat.WriteLine(option, Colors.bgMuted);
            }

            if (_descriptions != null) {
                Console.WriteLine("\n\n\n");
                _colorFormat.DivisionLine('-', Colors.bgDefault);
                Console.WriteLine(_descriptions[_options.IndexOf(_option)]);
            }
        }

        public void ReadInput(ConsoleKey consoleKey) {
            if (consoleKey == ConsoleKey.Enter) { 
                if (_actions != null) _actions[_options.IndexOf(_option)].Invoke(); 
            }

            else if (consoleKey == ConsoleKey.UpArrow) _option = _options[Math.Max(_options.IndexOf(_option) - 1, 0)];
            else if (consoleKey == ConsoleKey.DownArrow) _option = _options[Math.Min(_options.IndexOf(_option) + 1, _options.Count - 1)];
        }
    }
}
