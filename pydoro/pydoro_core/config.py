import argparse
import configparser
import os

from prompt_toolkit.key_binding import KeyBindings


class Configuration():
    def __init__(self):
        self._cliparse() # Parse arguments from command line
        self._iniparse() # Parse config (.ini) file
        self.kb = KeyBindings()

        # Load parsed configs (cli overrites ini)
        self._iniload()
        self._cliload()

    def _cliparse(self):
        """
        Parse configurations from command line arguments
        """
        parser = argparse.ArgumentParser("pydoro", description="Terminal Pomodoro Timer")
        parser.add_argument(
            "-e",
            "--emoji",
            action="store_true",
            help="If set, use tomato emoji instead of the ASCII art",
        )
        parser.add_argument(
            "--focus",
            help="focus mode: hides clock and \
                            mutes sounds (equivalent to --no-clock and --no-sound)",
            action="store_true",
        )
        parser.add_argument("--no-clock", help="hides clock", action="store_true")
        parser.add_argument("--no-sound", help="mutes all sounds", action="store_true")
        self.cliargs = parser.parse_args()

    def _iniparse(self):
        """
        Look at PYDORO_CONFIG_FILE environment variable
        Defaults to ~/.pydoro.ini if PYDORO_CONFIG_FILE not set
        """
        self._conf = configparser.ConfigParser()

        filename = os.path.expanduser("~/.pydoro.ini")

        if 'PYDORO_CONFIG_FILE' in os.environ:
            filename = os.environ['PYDORO_CONFIG_FILE']

        if os.path.exists(filename):
            self._conf.read(filename)
        else:
            print("Couldn't read config file. Creating it (" + filename + ")")
            self._create_default_ini()

    def _create_default_ini(self):
        """
        Creates default ini configuration file
        Saves it in '~/.pydoro.ini'
        """
        self._conf['DEFAULT'] = {}

        self._conf['General'] = {}
        self._conf['General']['no_clock'] = 'False'
        self._conf['General']['no_sound'] = 'False'
        self._conf['General']['emoji'] = 'False'

        self._conf['Time'] = {}
        self._conf['Time']['tomatoes_per_set'] = '4'
        self._conf['Time']['work_minutes'] = '25'
        self._conf['Time']['small_break_minutes'] = '5'
        self._conf['Time']['long_break_minutes'] = '15'
        self._conf['Time']['alarm_seconds'] = '20'

        self._conf['KeyBindings'] = {}
        self._conf['KeyBindings']['focus_previous'] = "s-tab,left,h,j"
        self._conf['KeyBindings']['focus_next'] = "tab,right,l,k"
        self._conf['KeyBindings']['exit_clicked'] = "q"

        # Write file
        filename = os.path.expanduser("~/.pydoro.ini")
        with open(filename, "w+") as configfile:
            self._conf.write(configfile)

    def _iniload(self):
        """
        Loads the .ini config file preferences

        Command line arguments override file configurations.
        """

        # Check for no-clock (or focus mode)
        self.no_clock = self._conf['General']['no_clock'] == 'True'

        # Check for no-sound (or focus mode)
        self.no_sound = self._conf['General']['no_sound'] == 'True'

        # Check for emoji
        self.emoji = self._conf['General']['emoji'] == 'True'

        # Load key bindings
        for action, keys in self._conf['KeyBindings'].items():
            # Split string from config file back into list
            keys = keys.split(',')
            for key in keys:
                self.kb.add(key.strip())(actions[action])

        self.tomatoes_per_set =
            int(self.conf['Time']['tomatoes_per_set'])
        self.work_minutes =
            int(self._conf['Time']['work_minutes'])
        self.small_break_minutes =
            int(self._conf['Time']['small_break_minutes'])
        self.long_break_minutes =
            int(self._conf['Time']['long_break_minutes'])
        self.alarm_seconds =
            int(self._conf['Time']['alarm_seconds'])

    def _cliload(self):
        """
        Loads the command line arguments

        Command line arguments override file configurations.
        """

        # Check for no-clock (or focus mode)
        self.no_clock = self.cliargs.no_clock or self.cliargs.focus

        # Check for no-sound (or focus mode)
        self.no_sound = self.cliargs.no_sound or self.cliargs.focus

        # Check for emoji
        self.emoji = cliargs.emoji


