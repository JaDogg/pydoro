"""Deterministic tests for skipping periods and configurable key bindings."""

import configparser
import tempfile
import unittest
from pathlib import Path
from threading import Event, Thread
from types import SimpleNamespace
from unittest.mock import Mock, patch

from prompt_toolkit.widgets import Label

from pydoro.pydoro_core.config import Configuration
from pydoro.pydoro_core.tomato import (
    InitialState,
    IntermediateState,
    LongBreakState,
    SmallBreakState,
    Tomato,
    WorkingState,
)
from pydoro.pydoro_tui import HelpContainer, UserInterface


class SkipTests(unittest.TestCase):
    def setUp(self):
        self.clock = patch("pydoro.pydoro_core.tomato.cur_time", return_value=100)
        self.clock.start()
        self.addCleanup(self.clock.stop)
        self.config = SimpleNamespace(
            no_sound=True,
            no_clock=False,
            emoji=False,
            work_minutes=25,
            small_break_minutes=5,
            long_break_minutes=15,
            alarm_seconds=20,
            tomatoes_per_set=4,
            work_state_cmd=[],
            work_paused_state_cmd=[],
            work_resumed_state_cmd=[],
            small_break_state_cmd=[],
            long_break_state_cmd=[],
        )
        self.tomato = Tomato(self.config)

    def test_initial_and_waiting_skip_are_noops(self):
        initial = self.tomato._state
        self.tomato.skip()
        self.assertIs(self.tomato._state, initial)
        self.assertIsInstance(initial, InitialState)
        self.tomato.start()
        self.tomato.skip()
        waiting = self.tomato._state
        self.tomato.skip()
        self.assertIs(self.tomato._state, waiting)
        self.assertIsInstance(waiting, IntermediateState)

    def test_work_skip_does_not_count_a_tomato_or_set(self):
        self.tomato.tomatoes = 3
        self.tomato.start()
        self.tomato.skip()
        self.assertEqual(self.tomato.tomatoes, 3)
        self.assertIsInstance(self.tomato._state, IntermediateState)
        self.tomato.update()
        self.tomato.start()
        self.assertIs(type(self.tomato._state), SmallBreakState)
        self.assertEqual(self.tomato._state.remainder, 300)
        self.assertEqual(self.tomato.tomatoes, 3)

    def test_breaks_and_paused_periods_skip_to_the_correct_successor(self):
        for state_type, next_type in (
            (WorkingState, SmallBreakState),
            (SmallBreakState, WorkingState),
            (LongBreakState, WorkingState),
        ):
            for paused in (False, True):
                with self.subTest(state=state_type, paused=paused):
                    self.tomato._state = state_type(self.tomato)
                    if paused:
                        self.tomato.pause()
                    self.tomato.skip()
                    self.assertIsInstance(self.tomato._state, IntermediateState)
                    self.tomato.start()
                    self.assertIs(type(self.tomato._state), next_type)
                    self.assertEqual(self.tomato.tomatoes, 0)

    def test_natural_completion_still_counts_and_schedules_long_break(self):
        self.tomato.tomatoes = 3
        self.tomato.start()
        self.tomato._state._remainder = 0
        self.tomato.update()
        self.assertEqual(self.tomato.tomatoes, 4)
        self.tomato.start()
        self.assertIs(type(self.tomato._state), LongBreakState)

    def test_skip_does_not_run_resume_or_next_period_commands(self):
        self.config.work_state_cmd = ["work-hook"]
        self.config.work_resumed_state_cmd = ["resume-hook"]
        self.config.small_break_state_cmd = ["break-hook"]
        with patch("pydoro.pydoro_core.tomato.subprocess.run") as run:
            self.tomato.start()
            self.tomato.pause()
            self.tomato.skip()
            run.assert_called_once_with(["work-hook"])
            self.tomato.start()
            self.assertEqual(run.call_count, 2)
            run.assert_called_with(["break-hook"])

    def test_reset_after_skip_is_unchanged(self):
        self.tomato.start()
        self.tomato.skip()
        self.tomato.start()
        self.tomato.reset()
        self.assertEqual(self.tomato._state.remainder, 300)
        self.tomato.reset_all()
        self.assertIs(type(self.tomato._state), InitialState)
        self.assertEqual(self.tomato.tomatoes, 0)

    def test_custom_skip_binding_calls_tomato(self):
        ui = UserInterface.__new__(UserInterface)
        ui.configs = SimpleNamespace(key_bindings={"skip": "n,c-n"})
        ui.tomato = Mock()
        ui._set_key_bindings()
        for key in ("n", "c-n"):
            binding = ui.kb.get_bindings_for_keys((key,))
            self.assertEqual(len(binding), 1)
            binding[0].handler(None)
        self.assertEqual(ui.tomato.skip.call_count, 2)

    def test_existing_ini_gets_default_and_can_override_skip(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "pydoro.ini"
            for text, expected in (
                ("[KeyBindings]\nstart = s\n", "n"),
                ("[KeyBindings]\nskip = c-n\n", "c-n"),
                ("[KeyBindings]\nskip =\n", ""),
            ):
                with self.subTest(text=text):
                    path.write_text(text, encoding="utf-8")
                    config = Configuration.__new__(Configuration)
                    with patch.dict("os.environ", {"PYDORO_CONFIG_FILE": str(path)}):
                        config._ini_parse()
                    self.assertEqual(config._conf["KeyBindings"]["skip"], expected)

    def test_empty_skip_binding_can_be_disabled(self):
        ui = UserInterface.__new__(UserInterface)
        ui.configs = SimpleNamespace(key_bindings={"skip": " "})
        ui.tomato = Mock()
        ui._set_key_bindings()
        self.assertEqual(ui.kb.bindings, [])

    def test_skip_and_update_are_serialized(self):
        for first_action in ("skip", "update"):
            with self.subTest(first_action=first_action):
                self.tomato = Tomato(self.config)
                self.tomato.start()
                self.tomato._state._remainder = 0
                entered, release, second_started, second_done = (
                    Event(),
                    Event(),
                    Event(),
                    Event(),
                )
                errors = []
                original_transition = IntermediateState.transition_to

                def blocked_transition(factory, tomato):
                    entered.set()
                    if not release.wait(5):
                        raise AssertionError("transition was not released")
                    return original_transition(factory, tomato)

                def invoke(action, second=False):
                    try:
                        if second:
                            second_started.set()
                        getattr(self.tomato, action)()
                    except Exception as error:
                        errors.append(error)
                    finally:
                        if second:
                            second_done.set()

                second_action = "update" if first_action == "skip" else "skip"
                first = Thread(target=invoke, args=(first_action,))
                second = Thread(target=invoke, args=(second_action, True))
                with patch.object(
                    IntermediateState, "transition_to", side_effect=blocked_transition
                ):
                    first.start()
                    try:
                        self.assertTrue(entered.wait(5))
                        second.start()
                        self.assertTrue(second_started.wait(5))
                        self.assertFalse(second_done.is_set())
                    finally:
                        release.set()
                        first.join(5)
                        if second.ident is not None:
                            second.join(5)
                self.assertFalse(first.is_alive())
                self.assertFalse(second.is_alive())
                self.assertEqual(errors, [])
                self.assertEqual(self.tomato.tomatoes, first_action == "update")
                self.assertIsInstance(self.tomato._state, IntermediateState)

    def test_help_shows_skip_shortcut(self):
        config = configparser.ConfigParser()
        config["KeyBindings"] = dict(
            start="s",
            pause="p",
            reset="r",
            reset_all="a",
            help="?",
            focus_previous="left",
            focus_next="right",
            exit_clicked="q",
            skip="c-n",
        )
        with patch("pydoro.pydoro_tui.Label", wraps=Label) as label:
            HelpContainer(config["KeyBindings"])
        label.assert_any_call(text="skip period   | c-n")


if __name__ == "__main__":
    unittest.main()
