#!/usr/bin/env python

__version__ = "0.2.3"

import sys
import threading
import subprocess

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import focus_next, focus_previous
from prompt_toolkit.layout import (
    HSplit,
    Layout,
    VSplit,
    FormattedTextControl,
    Window,
    ConditionalContainer,
)
from prompt_toolkit.filters import Condition
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Label

from pydoro.pydoro_core.config import Configuration
from pydoro.pydoro_core.tomato import Tomato
from pydoro.pydoro_core.util import every, in_app_path
import pydoro.pydoro_core.sound as sound


class UserInterface:
    def __init__(self, config: Configuration):
        self.config = config
        self.tomato = Tomato(self.config)
        self.prev_hash = None

        self.helpwindow = HelpContainer(self.config._conf["KeyBindings"])

        self._create_ui()

    def _create_ui(self):
        btn_start = Button("Start", handler=self.tomato.start)
        btn_pause = Button("Pause", handler=self.tomato.pause)
        btn_reset = Button("Reset", handler=self.tomato.reset)
        btn_reset_all = Button("Reset All", handler=self.tomato.reset_all)
        btn_exit = Button("Exit", handler=self._exit_clicked)
        # All the widgets for the UI.
        self.text_area = FormattedTextControl(focusable=False, show_cursor=False)
        text_window = Window(
            content=self.text_area,
            dont_extend_height=True,
            height=11,
            style="bg:#ffffff #000000",
        )
        root_container = Box(
            HSplit(
                [
                    Label(text="Press `Tab` to move the focus."),
                    HSplit(
                        [
                            VSplit(
                                [
                                    btn_start,
                                    btn_pause,
                                    btn_reset,
                                    btn_reset_all,
                                    btn_exit,
                                ],
                                padding=1,
                                style="bg:#cccccc",
                            ),
                            text_window,
                        ]
                    ),
                    self.helpwindow,
                ]
            )
        )

        layout = Layout(container=root_container, focused_element=btn_start)
        self._set_key_bindings()

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

        self.application = Application(
            layout=layout, key_bindings=self.kb, style=style, full_screen=True
        )

    def _set_key_bindings(self):
        self.kb = KeyBindings()

        actions = {
            "focus_next": focus_next,
            "focus_previous": focus_previous,
            "exit_clicked": self._exit_clicked,
            "start": lambda _=None: self.tomato.start(),
            "pause": lambda _=None: self.tomato.pause(),
            "reset": lambda _=None: self.tomato.reset(),
            "reset_all": lambda _=None: self.tomato.reset_all(),
            "help": lambda _=None: self.toggle_help_window_state(),
        }

        for action, keys in self.config.key_bindings.items():
            for key in keys.split(","):
                try:
                    self.kb.add(key.strip())(actions[action])
                except KeyError:
                    pass

    @staticmethod
    def _exit_clicked(_=None):
        get_app().exit()

    def toggle_help_window_state(self):
        if self.helpwindow.is_visible():
            self.helpwindow.hide()
        else:
            self.helpwindow.show()

    def _draw(self):
        self.tomato.update()
        text, hash_ = self.tomato.render()
        # WHY: Avoid unnecessary updates
        if hash_ != self.prev_hash:
            self.text_area.text = text
            self.application.invalidate()
            self.prev_hash = hash_

    def run(self):
        self._draw()
        threading.Thread(target=lambda: every(0.4, self._draw), daemon=True).start()
        self.application.run()


class HelpContainer(ConditionalContainer):
    def __init__(self, keybindings={}):
        self.visible = False

        content = Box(
            HSplit(
                [
                    Label(text=f"----------------Help------------------\n"),
                    Label(text=f"start         | {keybindings['start']}"),
                    Label(text=f"pause         | {keybindings['pause']}"),
                    Label(text=f"reset         | {keybindings['reset']}"),
                    Label(text=f"reset all     | {keybindings['reset_all']}"),
                    Label(text=f"help          | {keybindings['help']}"),
                    Label(text=f"focus prev    | {keybindings['focus_previous']}"),
                    Label(text=f"focus next    | {keybindings['focus_next']}"),
                    Label(text=f"exit          | {keybindings['exit_clicked']}"),
                ]
            )
        )

        @Condition
        def is_visible():
            return self.visible

        super().__init__(filter=is_visible, content=content)

    def is_visible(self):
        return self.visible

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False


def main():
    config = Configuration()
    if config.audio_check:
        # WHY twice: to catch more issues
        sound.play(in_app_path("b15.wav"), block=True)
        sound.play(in_app_path("b15.wav"), block=True)
        sys.exit(0)
    if config.show_version:
        print("pydoro : version - {0}".format(__version__))
        sys.exit(0)
    UserInterface(config).run()
    if config.exit_cmd:
        subprocess.run(config.exit_cmd)


if __name__ == "__main__":
    main()
