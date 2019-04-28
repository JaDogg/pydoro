#!/usr/bin/env python
"""
A simple example of a few buttons and click handlers.
"""
from __future__ import unicode_literals

import sys
import time
import threading
from timeit import default_timer as cur_time

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import (
    focus_next,
    focus_previous,
)
from prompt_toolkit.layout import HSplit, Layout, VSplit
from prompt_toolkit.styles import Style
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea

TOMATO = r"""
                   
      /'\/`\       
    .-  |/  -.     {status}
   /          \    {time}
  '            \   
 ;             ;   
 :          /  .   
  \       .'  /    {count}
    \ ____ .'      
                   
"""


def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task()
        except Exception:
            pass
            # in production code you might want to have this instead of course:
            # logger.exception("Problem while executing repetitive task.")
        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay


class Tomato:
    _TEXT = {"NONE": "Press start",
             "STARTED": "Started",
             "PAUSED": "Paused",
             "WORK": "Work", "SB": "Small Break", "LB": "Long Break", "NS": ""}

    def __init__(self, template=TOMATO, pomo=25, break_small=5, break_large=15):
        self._template = template
        self._pomo = pomo
        self._break_small = break_small
        self._break_large = break_large
        self._status = "NONE"
        self._started_at = 0
        self._cur_chunk = "NS"
        self._tomatoes = []

    def start(self):
        self._status = "STARTED"
        self._cur_chunk = "WORK"
        self._started_at = cur_time()
        # self.draw()

    def pause(self):
        self._status = "PAUSED"
        # self.draw()

    def reset(self):
        pass

    def reset_all(self):
        pass

    @property
    def time_remaining(self):
        cur = cur_time()
        remainder = self._pomo - ((cur - self._started_at) / 60.0)
        return "{0:00.2f} min remaining".format(remainder)

    @property
    def status(self):
        return self._TEXT[self._status] + " " + self._TEXT[self._cur_chunk]

    def as_text(self):
        return self._template.format(status=self.status, time=self.time_remaining, count="")

    def draw(self):
        text_area.text = self.as_text()


tomato = Tomato()


def exit_clicked():
    get_app().exit()


# All the widgets for the UI.
btn_start = Button('Start', handler=tomato.start)
btn_pause = Button('Pause', handler=tomato.pause)
btn_reset = Button('Reset', handler=tomato.reset)
btn_reset_all = Button('Reset All', handler=tomato.reset_all)
btn_exit = Button('Exit', handler=exit_clicked)
text_area = TextArea(read_only=True,
                     width=50,
                     focusable=False)
tomato.draw()

# Combine all the widgets in a UI.
# The `Box` object ensures that padding will be inserted around the containing
# widget. It adapts automatically, unless an explicit `padding` amount is given.
root_container = Box(
    HSplit([
        Label(text='Press `Tab` to move the focus.'),
        VSplit([
            Box(
                body=HSplit(
                    [btn_start, btn_pause, btn_reset, btn_reset_all, btn_exit],
                    padding=1),
                padding=1,
                style='class:left-pane'),
            Box(
                body=Frame(text_area),
                padding=1,
                style='class:right-pane'),
        ]),
    ]),
)

layout = Layout(
    container=root_container,
    focused_element=btn_start)

# Key bindings.
kb = KeyBindings()
kb.add('tab')(focus_next)
kb.add('s-tab')(focus_previous)

# Styling.
style = Style([
    ('left-pane', 'bg:#888800 #000000'),
    ('right-pane', 'bg:#00aa00 #000000'),
    ('button', '#000000'),
    ('button-arrow', '#000000'),
    ('button focused', 'bg:#ff0000'),
    ('text-area focused', 'bg:#ff0000'),
    ('red', '#ff0000'),
    ('green', '#00ff00')
])

# Build a main application object.
application = Application(
    layout=layout,
    key_bindings=kb,
    style=style,
    full_screen=True)


def main():
    threading.Thread(target=lambda: every(0.5, tomato.draw), daemon=True).start()
    application.run()


if __name__ == '__main__':
    main()
