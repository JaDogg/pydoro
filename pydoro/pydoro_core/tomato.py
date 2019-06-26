import itertools
from enum import IntEnum
from timeit import default_timer

from pydoro.pydoro_core import sound
from pydoro.pydoro_core.util import in_app_path

TOMATOES_PER_SET = 4
SECONDS_PER_MIN = 60
WORK_TIME = 25 * SECONDS_PER_MIN
SMALL_BREAK_TIME = 5 * SECONDS_PER_MIN
LONG_BREAK_TIME = 15 * SECONDS_PER_MIN
ALARM_TIME = 20


TOMATO = [
    ("", "\n      "),
    ("#00cc00", "/'\\/`\\"),
    ("", "         "),
    ("", "task1"),
    ("", "\n    "),
    ("#ff0000", ".-"),
    ("", "  "),
    ("#00cc00", "|/"),
    ("", "  "),
    ("#ff0000", "-."),
    ("", "       "),
    ("", "task2"),
    ("", "\n   "),
    ("#ff0000", "/"),
    ("", "          "),
    ("#ff0000", "\\"),
    ("", "      "),
    ("", "task3"),
    ("", "\n  "),
    ("#ff0000", "'"),
    ("", "   "),
    ("bold", "pydoro"),
    ("", "   "),
    ("#ff0000", "\\"),
    ("", "     "),
    ("", "task4"),
    ("", "\n "),
    ("#ff0000", ";"),
    ("", "             "),
    ("#ff0000", "'"),
    ("", "     "),
    ("", "status"),
    ("", "\n "),
    ("#ff0000", ";"),
    ("", "             "),
    ("#ff0000", ";"),
    ("", "     "),
    ("", "time"),
    ("", "\n "),
    ("#ff0000", ":"),
    ("", "          "),
    ("#ff0000", "/"),
    ("", "  "),
    ("#ff0000", "."),
    ("", "\n  "),
    ("#ff0000", "\\"),
    ("", "       "),
    ("#ff0000", ".'"),
    ("", "  "),
    ("#ff0000", "/"),
    ("", "      "),
    ("", "count"),
    ("", "\n    "),
    ("#ff0000", "\\"),
    ("", " "),
    ("#ff0000", "____"),
    ("", " "),
    ("#ff0000", ".'"),
    ("", "        "),
    ("", "sets"),
]

LOCATIONS = {
    "count": 51,
    "sets": 59,
    "status": 31,
    "task1": 3,
    "task2": 11,
    "task3": 17,
    "task4": 25,
    "time": 37,
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
    TaskStatus.NONE.value: "",
    TaskStatus.STARTED.value: "",
    TaskStatus.PAUSED.value: "PAUSED",
    TaskStatus.LIMBO.value: "",
    Tasks.WORK.value: TEXT_WORK,
    Tasks.SMALL_BREAK.value: TEXT_SMALL_BREAK,
    Tasks.LONG_BREAK.value: TEXT_LONG_BREAK,
    Tasks.NO_TASK.value: "",
    Tasks.INTERMEDIATE.value: "",
}

PROGRESS = ["|#  |", "| # |", "|  #|", "| # |"]


def cur_time():
    return int(default_timer())


def play_alarm():
    # noinspection PyBroadException
    try:
        sound.play(in_app_path("b15.wav"), block=False)
    except Exception:
        pass


class InitialState:
    name = "initial"

    def __init__(self, time_period=0, tomato=None):
        self._time_period = int(time_period)
        self._tomato = tomato
        self._task = Tasks.NO_TASK
        self._status = TaskStatus.NONE
        self._started_at = 0
        self._remainder = 0
        self._progress = itertools.cycle(PROGRESS)

    def start(self):
        play_alarm()
        return WorkingState(tomato=self._tomato)

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
        difference = cur - self._started_at
        remainder = self._remainder - difference
        self._started_at = cur
        if remainder <= 0:
            remainder = 0
        self._remainder = remainder


class IntermediateState(InitialState):
    name = "waiting"

    def __init__(self, time_period=0, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
        self._task = Tasks.INTERMEDIATE
        self._status = TaskStatus.LIMBO
        self._next_factory = None
        self._last_alarm_time = 0
        self._sound()

    def _sound(self):
        if cur_time() - self._last_alarm_time > ALARM_TIME:
            play_alarm()
            self._last_alarm_time = cur_time()

    def start(self):
        return self._next_factory(tomato=self._tomato)

    @property
    def time_remaining(self):
        self._sound()
        return "Press [start] to continue with " + self._next_factory.name

    @property
    def done(self):
        return False

    @staticmethod
    def transition_to(next_state_factory, tomato):
        state = IntermediateState(tomato=tomato)
        state._next_factory = next_state_factory
        return state


class WorkingState(InitialState):
    name = "work"

    def __init__(self, time_period=WORK_TIME, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
        self._remainder = int(self._time_period)
        self._task = Tasks.WORK
        self._status = TaskStatus.STARTED
        self._started_at = cur_time()

    def start(self):
        return self

    @property
    def time_remaining(self):
        self._calc_remainder()

        return self._format_time(self._remainder)

    @property
    def next_state(self):
        self._tomato.tomatoes += 1
        if self._tomato.tomatoes % TOMATOES_PER_SET == 0:
            return IntermediateState.transition_to(LongBreakState, tomato=self._tomato)
        return IntermediateState.transition_to(SmallBreakState, tomato=self._tomato)

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

    def __init__(self, time_period=0, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
        self._prev = None
        self._task = Tasks.WORK
        self._status = TaskStatus.PAUSED

    def start(self):
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
        cur_state = WorkPausedState(tomato=tomato)
        cur_state._prev = state
        return cur_state

    @property
    def done(self):
        return False


class SmallBreakState(InitialState):
    name = "small break"

    def __init__(self, time_period=SMALL_BREAK_TIME, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
        self._remainder = int(self._time_period)
        self._task = Tasks.SMALL_BREAK
        self._status = TaskStatus.STARTED
        self._started_at = cur_time()

    def start(self):
        return self

    @property
    def time_remaining(self):
        self._calc_remainder()

        return self._format_time(self._remainder)

    @property
    def next_state(self):
        return IntermediateState.transition_to(WorkingState, tomato=self._tomato)

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

    def __init__(self, time_period=0, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
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
        cur_state = SmallBreakPausedState(tomato=tomato)
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

    def __init__(self, time_period=LONG_BREAK_TIME, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
        self._task = Tasks.LONG_BREAK
        self._status = TaskStatus.STARTED

    def pause(self):
        return LongBreakPausedState.return_to(self._tomato, self)


class LongBreakPausedState(SmallBreakPausedState):
    name = "long break paused"

    def __init__(self, time_period=0, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
        self._task = Tasks.LONG_BREAK
        self._status = TaskStatus.PAUSED

    @staticmethod
    def return_to(tomato, state):
        cur_state = LongBreakPausedState(tomato=tomato)
        cur_state._prev = state
        return cur_state


class Tomato:
    def __init__(self):
        self._state = InitialState(tomato=self)
        self.tomatoes = 0

    def start(self):
        self._state = self._state.start()

    def pause(self):
        self._state = self._state.pause()

    def reset(self):
        self._state = self._state.reset()

    def reset_all(self):
        self._state = InitialState(tomato=self)
        self.tomatoes = 0

    def update(self):
        if self._state.done:
            self._state = self._state.next_state

    def as_formatted_text(self):
        task = TEXT[self._state.task.value]
        task = task.splitlines()
        if not task:
            task = [""] * 4

        sets = self.tomatoes // TOMATOES_PER_SET
        if sets == 1:
            sets = "1 set completed"
        elif sets >= 2:
            sets = str(sets) + " sets completed"
        else:
            sets = ""

        status = TEXT[self._state.status.value]
        time = self._state.time_remaining
        count = "(`) " * (TOMATOES_PER_SET - self.tomatoes % TOMATOES_PER_SET)

        ftext = TOMATO[:]
        for i in range(1, 5):
            ftext[LOCATIONS["task" + str(i)]] = ("", task[i - 1])
        ftext[LOCATIONS["status"]] = ("", status)
        ftext[LOCATIONS["time"]] = ("", time)
        ftext[LOCATIONS["count"]] = ("", count)
        ftext[LOCATIONS["sets"]] = ("", sets)

        return ftext
