import argparse
import configparser
import os

from pydoro.pydoro_core.util import in_app_path


class Configuration:
    def __init__(self):
        self._cli_parse()
        self._ini_parse()
        self._ini_load()
        self._cli_load()

    def _cli_parse(self):
        """
        Parse command line arguments
        """
        parser = argparse.ArgumentParser(
            "pydoro", description="Terminal Pomodoro Timer"
        )
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
        parser.add_argument(
            "--audio-check", help="play audio and exit", action="store_true"
        )
        parser.add_argument(
            "--version", help="display version and exit", action="store_true"
        )
        parser.add_argument("--audio-file", metavar='path', help="custom audio file")
        self.cli_args = parser.parse_args()

    def _ini_parse(self):
        """
        Parse configuration file
        Look at PYDORO_CONFIG_FILE environment variable
        Defaults to ~/.pydoro.ini if PYDORO_CONFIG_FILE not set
        """
        self._conf = configparser.ConfigParser()

        filename = os.environ.get(
            "PYDORO_CONFIG_FILE", os.path.expanduser("~/.pydoro.ini")
        )

        if os.path.exists(filename):
            self._conf.read(filename)
        else:
            self._create_default_ini()

    def _create_default_ini(self):
        """
        Creates default ini configuration file
        Saves it in '~/.pydoro.ini'
        """
        self._conf["DEFAULT"] = {}

        self._conf["General"] = {}
        self._conf["General"]["no_clock"] = "False"
        self._conf["General"]["no_sound"] = "False"
        self._conf["General"]["emoji"] = "False"

        self._conf["Time"] = {}
        self._conf["Time"]["tomatoes_per_set"] = "4"
        self._conf["Time"]["work_minutes"] = "25"
        self._conf["Time"]["small_break_minutes"] = "5"
        self._conf["Time"]["long_break_minutes"] = "15"
        self._conf["Time"]["alarm_seconds"] = "20"

        self._conf["KeyBindings"] = {}
        self._conf["KeyBindings"]["focus_previous"] = "s-tab,left,h,j"
        self._conf["KeyBindings"]["focus_next"] = "tab,right,l,k"
        self._conf["KeyBindings"]["exit_clicked"] = "q"
        self._conf["KeyBindings"]["start"] = "s"
        self._conf["KeyBindings"]["pause"] = "p"
        self._conf["KeyBindings"]["reset"] = "r"
        self._conf["KeyBindings"]["reset_all"] = "a"

        filename = os.path.expanduser("~/.pydoro.ini")
        with open(filename, "w+") as configfile:
            self._conf.write(configfile)

    def _ini_load(self):
        """
        Loads the .ini config file preferences

        Command line arguments override file configurations.
        """
        self.no_clock = self._conf["General"]["no_clock"] == "True"
        self.no_sound = self._conf["General"]["no_sound"] == "True"
        self.emoji = self._conf["General"]["emoji"] == "True"
        self.tomatoes_per_set = int(self._conf["Time"]["tomatoes_per_set"])
        self.work_minutes = float(self._conf["Time"]["work_minutes"])
        self.small_break_minutes = float(self._conf["Time"]["small_break_minutes"])
        self.long_break_minutes = float(self._conf["Time"]["long_break_minutes"])
        self.alarm_seconds = int(self._conf["Time"]["alarm_seconds"])
        self.key_bindings = self._conf["KeyBindings"]

    def _cli_load(self):
        """
        Loads the command line arguments

        Command line arguments override file configurations.
        """
        self.no_clock = self.cli_args.no_clock or self.cli_args.focus or self.no_clock
        self.no_sound = self.cli_args.no_sound or self.cli_args.focus or self.no_sound
        self.emoji = self.cli_args.emoji or self.emoji
        self.audio_check = self.cli_args.audio_check
        self.show_version = self.cli_args.version
        self.audio_file = self.cli_args.audio_file or in_app_path("b15.wav")