using Colorify;
using Colorify.UI;
using CordellRadioTelescope.EXMPL.window;
using Figgle;


namespace CordellRadioTelescope.EXMPL {
    public class Program {
        public static void Main(string[] args) {
            window = new ProgramWindow(ConsoleColor.White, new Format(Theme.Light));
            window.DrawMainWindow();
        }

        private static ProgramWindow window;
    }
}
