import itertools
import subprocess
import sys
from enum import IntEnum
from timeit import default_timer

from pydoro.pydoro_core import sound
from pydoro.pydoro_core.util import in_app_path
from pydoro.pydoro_core.config import Configuration

SECONDS_PER_MIN = 60

PLACEHOLDER_TIME = "time"
PLACEHOLDER_STATUS = "status"
PLACEHOLDER_SETS = "sets"
PLACEHOLDER_COUNT = "count"
PLACEHOLDER_TASK = "task1", "task2", "task3", "task4"

NO_COLOUR = ""
RED = "#ff0000"
GREEN = "#00cc00"
BOLD_TEXT = "bold"

# Tomato ascii art
#   tuples is made of colour and a piece of coloured text
TOMATO = [
    (NO_COLOUR, "\n      "),
    (GREEN, "/'\\/`\\"),
    (NO_COLOUR, "         "),
    (NO_COLOUR, PLACEHOLDER_TASK[0]),
    (NO_COLOUR, "\n    "),
    (RED, ".-"),
    (NO_COLOUR, "  "),
    (GREEN, "|/"),
    (NO_COLOUR, "  "),
    (RED, "-."),
    (NO_COLOUR, "       "),
    (NO_COLOUR, PLACEHOLDER_TASK[1]),
    (NO_COLOUR, "\n   "),
    (RED, "/"),
    (NO_COLOUR, "          "),
    (RED, "\\"),
    (NO_COLOUR, "      "),
    (NO_COLOUR, PLACEHOLDER_TASK[2]),
    (NO_COLOUR, "\n  "),
    (RED, "'"),
    (NO_COLOUR, "   "),
    (BOLD_TEXT, "pydoro"),
    (NO_COLOUR, "   "),
    (RED, "\\"),
    (NO_COLOUR, "     "),
    (NO_COLOUR, PLACEHOLDER_TASK[3]),
    (NO_COLOUR, "\n "),
    (RED, ";"),
    (NO_COLOUR, "             "),
    (RED, "'"),
    (NO_COLOUR, "     "),
    (NO_COLOUR, PLACEHOLDER_STATUS),
    (NO_COLOUR, "\n "),
    (RED, ";"),
    (NO_COLOUR, "             "),
    (RED, ";"),
    (NO_COLOUR, "     "),
    (NO_COLOUR, PLACEHOLDER_TIME),
    (NO_COLOUR, "\n "),
    (RED, ":"),
    (NO_COLOUR, "          "),
    (RED, "/"),
    (NO_COLOUR, "  "),
    (RED, "."),
    (NO_COLOUR, "\n  "),
    (RED, "\\"),
    (NO_COLOUR, "       "),
    (RED, ".'"),
    (NO_COLOUR, "  "),
    (RED, "/"),
    (NO_COLOUR, "      "),
    (NO_COLOUR, PLACEHOLDER_COUNT),
    (NO_COLOUR, "\n    "),
    (RED, "\\"),
    (NO_COLOUR, " "),
    (RED, "____"),
    (NO_COLOUR, " "),
    (RED, ".'"),
    (NO_COLOUR, "        "),
    (NO_COLOUR, PLACEHOLDER_SETS),
]

LOCATIONS = {
    PLACEHOLDER_COUNT: 51,
    PLACEHOLDER_SETS: 59,
    PLACEHOLDER_STATUS: 31,
    PLACEHOLDER_TASK[0]: 3,
    PLACEHOLDER_TASK[1]: 11,
    PLACEHOLDER_TASK[2]: 17,
    PLACEHOLDER_TASK[3]: 25,
    PLACEHOLDER_TIME: 37,
}

TEXT_LONG_BREAK = r"""
  ___    LONG      _
 | _ )_ _ ___ __ _| |__
 | _ | '_/ -_/ _` | / /
 |___|_| \___\__,_|_\_\
""".strip(
    "\r\n"
)

TEXT_SMALL_BREAK = TEXT_LONG_BREAK.replace("LONG", "SMALL")

TEXT_WORK = r"""
 __      __       _
 \ \    / ___ _ _| |__
  \ \/\/ / _ | '_| / /
   \_/\_/\___|_| |_\_\
""".strip(
    "\r\n"
)


class Tasks(IntEnum):
    WORK = 1
    SMALL_BREAK = 2
    LONG_BREAK = 3
    NO_TASK = 4
    INTERMEDIATE = 5


class TaskStatus(IntEnum):
    NONE = 111
    STARTED = 222
    PAUSED = 555
    LIMBO = 666


TEXT = {
    TaskStatus.NONE: "",
    TaskStatus.STARTED: "",
    TaskStatus.PAUSED: "PAUSED",
    TaskStatus.LIMBO: "",
    Tasks.WORK: TEXT_WORK,
    Tasks.SMALL_BREAK: TEXT_SMALL_BREAK,
    Tasks.LONG_BREAK: TEXT_LONG_BREAK,
    Tasks.NO_TASK: "",
    Tasks.INTERMEDIATE: "",
}

PROGRESS = ["|#  |", "| # |", "|  #|", "| # |"]


def cur_time():
    return int(default_timer())


class InitialState:
    name = "initial"

    def __init__(self, tomato):
        self._tomato = tomato
        self._task = Tasks.NO_TASK
        self._status = TaskStatus.NONE
        self._started_at = 0
        self._remainder = 0
        self._time_period = 0
        self._progress = itertools.cycle(PROGRESS)

    def start(self):
        self._tomato.play_alarm()
        return WorkingState(self._tomato)

    def pause(self):
        return self

    def reset(self):
        return self

    @property
    def remainder(self):
        return self._remainder

    @property
    def next_state(self):
        return self

    @property
    def time_period(self):
        return self._time_period

    @property
    def time_remaining(self):
        return "Press [start]"

    @property
    def task(self):
        return self._task

    @property
    def status(self):
        return self._status

    @property
    def done(self):
        return False

    def _format_time(self, remainder):
        minutes, seconds = divmod(int(remainder), SECONDS_PER_MIN)
        if self.status == TaskStatus.STARTED:
            progress = next(self._progress) + " "
        else:
            progress = ""

        return "{}{:00}min {:00}s remaining".format(progress, minutes, seconds)

    def _calc_remainder(self):
        cur = cur_time()
        self._remainder = max(self._remainder - (cur - self._started_at), 0)
        self._started_at = cur


class IntermediateState(InitialState):
    name = "waiting"

    def __init__(self, tomato):
        super().__init__(tomato)
        self._task = Tasks.INTERMEDIATE
        self._status = TaskStatus.LIMBO
        self._next_factory = None
        self._last_alarm_time = 0
        self._sound()

    def _sound(self):
        if cur_time() - self._last_alarm_time > self._tomato.configs.alarm_seconds:
            self._tomato.play_alarm()
            self._last_alarm_time = cur_time()

    def start(self):
        return self._next_factory(self._tomato)

    @property
    def time_remaining(self):
        self._sound()
        return "Press [start] to continue with " + self._next_factory.name

    @property
    def done(self):
        return False

    @staticmethod
    def transition_to(next_state_factory, tomato):
        state = IntermediateState(tomato)
        state._next_factory = next_state_factory
        return state


class WorkingState(InitialState):
    name = "work"

    def __init__(self, tomato):
        super().__init__(tomato)
        self._time_period = self._remainder = int(
            self._tomato.configs.work_minutes * SECONDS_PER_MIN
        )
        self._task = Tasks.WORK
        self._status = TaskStatus.STARTED
        self._started_at = cur_time()
        if self._tomato.configs.work_state_cmd:
            subprocess.run(self._tomato.configs.work_state_cmd)

    def start(self):
        return self

    @property
    def time_remaining(self):
        self._calc_remainder()
        if self._tomato.no_clock:
            return ""
        return self._format_time(self._remainder)

    @property
    def next_state(self):
        self._tomato.tomatoes += 1
        if self._tomato.tomatoes % self._tomato.tomatoes_per_set == 0:
            return IntermediateState.transition_to(LongBreakState, self._tomato)
        return IntermediateState.transition_to(SmallBreakState, self._tomato)

    def pause(self):
        return WorkPausedState.return_to(self._tomato, self)

    def reset(self):
        self._remainder = self.time_period
        return self

    @property
    def done(self):
        return self._remainder <= 0


class WorkPausedState(InitialState):
    name = "work paused"

    def __init__(self, tomato):
        super().__init__(tomato)
        self._prev = None
        self._task = Tasks.WORK
        self._status = TaskStatus.PAUSED
        if self._tomato.configs.work_paused_state_cmd:
            subprocess.run(self._tomato.configs.work_paused_state_cmd)

    def start(self):
        if self._tomato.configs.work_resumed_state_cmd:
            subprocess.run(self._tomato.configs.work_resumed_state_cmd)
        self._prev._started_at = cur_time()
        return self._prev

    def reset(self):
        self._prev._remainder = self._prev.time_period
        return self

    @property
    def time_remaining(self):
        return self._format_time(self._prev.remainder)

    @staticmethod
    def return_to(tomato, state):
        cur_state = WorkPausedState(tomato)
        cur_state._prev = state
        return cur_state

    @property
    def done(self):
        return False


class SmallBreakState(InitialState):
    name = "small break"

    def __init__(self, tomato):
        super().__init__(tomato)
        self._time_period = self._remainder = int(
            self._tomato.configs.small_break_minutes * SECONDS_PER_MIN
        )
        self._task = Tasks.SMALL_BREAK
        self._status = TaskStatus.STARTED
        self._started_at = cur_time()
        if self._tomato.configs.small_break_state_cmd:
            subprocess.run(self._tomato.configs.small_break_state_cmd)

    def start(self):
        return self

    @property
    def time_remaining(self):
        self._calc_remainder()

        return self._format_time(self._remainder)

    @property
    def next_state(self):
        return IntermediateState.transition_to(WorkingState, self._tomato)

    def pause(self):
        return SmallBreakPausedState.return_to(self._tomato, self)

    def reset(self):
        self._remainder = self.time_period
        return self

    @property
    def done(self):
        return self._remainder <= 0


class SmallBreakPausedState(InitialState):
    name = "small break paused"

    def __init__(self, tomato):
        super().__init__(tomato)
        self._task = Tasks.SMALL_BREAK
        self._status = TaskStatus.PAUSED
        self._prev = None

    def start(self):
        self._prev._started_at = cur_time()
        return self._prev

    @property
    def time_remaining(self):
        return self._format_time(self._prev.remainder)

    @staticmethod
    def return_to(tomato, state):
        cur_state = SmallBreakPausedState(tomato)
        cur_state._prev = state
        return cur_state

    def reset(self):
        self._prev._remainder = self._prev.time_period
        return self

    @property
    def done(self):
        return False


class LongBreakState(SmallBreakState):
    name = "long break"

    def __init__(self, tomato):
        super().__init__(tomato)
        self._time_period = self._remainder = int(
            self._tomato.configs.long_break_minutes * SECONDS_PER_MIN
        )
        self._task = Tasks.LONG_BREAK
        self._status = TaskStatus.STARTED
        if self._tomato.configs.long_break_state_cmd:
            subprocess.run(self._tomato.configs.long_break_state_cmd)

    def pause(self):
        return LongBreakPausedState.return_to(self._tomato, self)


class LongBreakPausedState(SmallBreakPausedState):
    name = "long break paused"

    def __init__(self, tomato):
        super().__init__(tomato)
        self._task = Tasks.LONG_BREAK
        self._status = TaskStatus.PAUSED

    @staticmethod
    def return_to(tomato, state):
        cur_state = LongBreakPausedState(tomato)
        cur_state._prev = state
        return cur_state


class Tomato:
    def __init__(self, configs: Configuration):
        self.configs = configs
        self.no_sound = configs.no_sound
        self.emoji = configs.emoji
        self.tomatoes_per_set = configs.tomatoes_per_set
        self.no_clock = configs.no_clock
        self.tomatoes = 0

        self._state = InitialState(self)

    def start(self):
        self._state = self._state.start()

    def pause(self):
        self._state = self._state.pause()

    def reset(self):
        self._state = self._state.reset()

    def reset_all(self):
        self._state = InitialState(self)
        self.tomatoes = 0

    def update(self):
        if self._state.done:
            self._state = self._state.next_state

    def play_alarm(self):
        if self.no_sound:
            return
        # noinspection PyBroadException
        try:
            sound.play(self.configs.audio_file, block=False)
        except Exception:
            pass

    def tomato_symbol(self):
        ascii_tomato = "(`) "
        if self.emoji:
            try:
                "🍅".encode(sys.stdout.encoding)
                return "🍅 "
            except UnicodeEncodeError:
                return ascii_tomato
        return ascii_tomato

    def render(self) -> (list, int):
        task = TEXT[self._state.task]
        task = task.splitlines()
        if not task:
            task = [""] * 4

        sets = self.tomatoes // self.tomatoes_per_set
        if sets == 1:
            sets = "1 set completed"
        elif sets >= 2:
            sets = str(sets) + " sets completed"
        else:
            sets = ""

        status = TEXT[self._state.status]
        time = self._state.time_remaining
        count = self.tomato_symbol() * (
            self.tomatoes_per_set - self.tomatoes % self.tomatoes_per_set
        )

        ftext = TOMATO[:]
        for i in range(0, 4):
            ftext[LOCATIONS[PLACEHOLDER_TASK[i]]] = ("", task[i])
        ftext[LOCATIONS[PLACEHOLDER_STATUS]] = ("", status)
        ftext[LOCATIONS[PLACEHOLDER_TIME]] = ("", time)
        ftext[LOCATIONS[PLACEHOLDER_COUNT]] = ("", count)
        ftext[LOCATIONS[PLACEHOLDER_SETS]] = ("", sets)

        hash_ = hash((status, time, count, sets) + tuple(task))

        return ftext, hash_
