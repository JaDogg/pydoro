#!/usr/bin/env python
import threading

import argparse

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import HSplit, Layout, VSplit, FormattedTextControl, Window, ConditionalContainer
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Label

from pydoro.pydoro_core.tomato import Tomato
from pydoro.pydoro_core.util import every
from pydoro.pydoro_core.config import DEFAULT_KEY_BINDINGS

import configparser
import os


tomato = Tomato()


def exit_clicked(_=None):
    get_app().exit()


# All the widgets for the UI.
btn_start = Button("Start", handler=tomato.start)
btn_pause = Button("Pause", handler=tomato.pause)
btn_reset = Button("Reset", handler=tomato.reset)
btn_reset_all = Button("Reset All", handler=tomato.reset_all)
btn_exit = Button("Exit", handler=exit_clicked)

text_area = FormattedTextControl(focusable=False, show_cursor=False)
text_window = Window(
    content=text_area, dont_extend_height=True, height=11, style="bg:#ffffff #000000"
)

root_container = Box(
    HSplit(
        [
            Label(text="Press `Tab` to move the focus."),
            HSplit(
                [
                    VSplit(
                        [btn_start, btn_pause, btn_reset, btn_reset_all, btn_exit],
                        padding=1,
                        style="bg:#cccccc",
                    ),
                    text_window,
                ]
            ),
        ]
    )
)

layout = Layout(container=root_container, focused_element=btn_start)

# Key bindings. These values are set in pydoro_core/config.py.
kb = KeyBindings()

# WHY: string to action map to allow for easy configuration
actions = {
    "focus_next": focus_next,
    "focus_previous": focus_previous,
    "exit_clicked": exit_clicked,
}

for action, keys in DEFAULT_KEY_BINDINGS.items():
    for key in keys:
        kb.add(key)(actions[action])

# Styling.
style = Style(
    [
        ("left-pane", "bg:#888800 #000000"),
        ("right-pane", "bg:#00aa00 #000000"),
        ("button", "#000000"),
        ("button-arrow", "#000000"),
        ("button focused", "bg:#ff0000"),
        ("red", "#ff0000"),
        ("green", "#00ff00"),
    ]
)

# Build a main application object.
application = Application(layout=layout, key_bindings=kb, style=style, full_screen=True)


def create_default_config(config):
    config = configparser.ConfigParser()

    config['DEFAULT'] = {
        'test': True,
    }
    homedir = os.path.expanduser("~")
    with open(homedir + "/.pydoro.ini", "w+") as configfile:
        config.write(configfile)


def get_config_file():
    """
    Look at PYDORO_CONFIG_FILE environment variable
    Defaults to ~/.pydoro.ini if PYDORO_CONFIG_FILE not set
    """
    config = configparser.ConfigParser()

    filename = os.path.expanduser("~/.pydoro.ini")

    if 'PYDORO_CONFIG_FILE' in os.environ:
        filename = os.environ['PYDORO_CONFIG_FILE']

    if os.path.exists(filename):
        config.read(filename)
    else:
        print("Couldn't read config file. Creating it (" + filename + ")")
        create_default_config(config)

    return config


# Set/Read config file
config = get_config_file()

print(config.sections()) # testing
print(config['DEFAULT'])# testing


def draw():
    tomato.update()
    text_area.text = tomato.as_formatted_text()
    application.invalidate()


def main():
    # Parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("--focus", help="focus mode: hides clock and \
                        mutes sounds (equivalent to --no-clock and --no-sound)",
                        action="store_true")
    parser.add_argument("--no-clock", help="hides clock",
                        action="store_true")
    parser.add_argument("--no-sound", help="mutes all sounds",
                        action="store_true")
    args = parser.parse_args()

    # Check for no-clock (or focus mode)
    if args.no_clock or args.focus:
        tomato._no_clock = True

    # Check for no-sound (or focus mode)
    if args.no_sound or args.focus:
        tomato._no_sound = True

    draw()
    threading.Thread(target=lambda: every(0.4, draw), daemon=True).start()
    application.run()


if __name__ == "__main__":
    main()
