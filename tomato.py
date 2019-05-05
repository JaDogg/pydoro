import itertools
from enum import IntEnum
from timeit import default_timer as cur_time

TOMATOES_PER_SET = 4
SECONDS_PER_MIN = 60

TOMATO = r"""
      /'\/`\         {task1}
    .-  |/  -.       {task2}
   /          \      {task3}
  '   PyDoro   \     {task4}
 ;             '     {status}
 ;             ;     {time}
 :          /  .
  \       .'  /      {count}
    \ ____ .'        {sets}

"""

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


class InitialState:
    def __init__(self, time_period=0, tomato=None):
        self._time_period = int(time_period)
        self._tomato = tomato
        self._task = Tasks.NO_TASK
        self._status = TaskStatus.NONE
        self._started_at = 0
        self._remainder = 0
        self._progress = itertools.cycle(PROGRESS)

    def start(self):
        return WorkingState(tomato=self._tomato)

    def pause(self):
        return self

    def reset(self):
        return self

    @property
    def next_state(self):
        return self

    @property
    def time_remaining(self):
        return "Press <start>"

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
    def __init__(self, time_period=0, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
        self._task = Tasks.INTERMEDIATE
        self._status = TaskStatus.LIMBO
        self._next_factory = None

    def start(self):
        return self._next_factory(tomato=self._tomato)

    @property
    def time_remaining(self):
        return "Press <start> to continue"

    @property
    def done(self):
        return False

    @property
    def whats_next(self):
        if self._next_factory == WorkingState:
            return TEXT[Tasks.WORK.value]
        elif self._next_factory == SmallBreakState:
            return TEXT[Tasks.SMALL_BREAK.value]
        elif self._next_factory == LongBreakState:
            return TEXT[Tasks.LONG_BREAK.value]

    @staticmethod
    def transition_to(next_state_factory, tomato):
        state = IntermediateState(tomato=tomato)
        state._next_factory = next_state_factory
        return state


class WorkingState(InitialState):
    def __init__(self, time_period=0.1 * 60, tomato=None):
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
    def remainder(self):
        return self._remainder

    @property
    def next_state(self):
        self._tomato.tomatoes += 1
        if self._tomato.tomatoes % TOMATOES_PER_SET == 0:
            return IntermediateState.transition_to(LongBreakState, tomato=self._tomato)
        return IntermediateState.transition_to(SmallBreakState, tomato=self._tomato)

    def pause(self):
        return WorkPausedState.return_to(self._tomato, self)

    def reset(self):
        self._remainder = self._time_period
        return self

    @property
    def done(self):
        return int(self._remainder) <= 0


class WorkPausedState(InitialState):
    def __init__(self, time_period=1, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
        self._prev = None
        self._task = Tasks.WORK
        self._status = TaskStatus.PAUSED

    def start(self):
        self._prev._started_at = cur_time()
        return self._prev

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
    def __init__(self, time_period=0.1 * 60, tomato=None):
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
    def remainder(self):
        return self._remainder

    @property
    def next_state(self):
        return IntermediateState.transition_to(WorkingState, tomato=self._tomato)

    def pause(self):
        return SmallBreakPausedState.return_to(self._tomato, self)

    def reset(self):
        self._remainder = self._time_period
        return self

    @property
    def done(self):
        return int(self._remainder) <= 0


class SmallBreakPausedState(InitialState):
    def __int__(self, time_period=1, tomato=None):
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

    @property
    def done(self):
        return False


class LongBreakState(SmallBreakState):
    def __init__(self, time_period=0.1 * 60, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
        self._task = Tasks.LONG_BREAK
        self._status = TaskStatus.STARTED


class LongBreakPausedState(SmallBreakPausedState):
    def __int__(self, time_period=1, tomato=None):
        super().__init__(time_period=time_period, tomato=tomato)
        self._task = Tasks.LONG_BREAK
        self._status = TaskStatus.PAUSED


class Tomato:
    def __init__(self, template=TOMATO):
        self._template = template
        self._state = InitialState(tomato=self)
        self.tomatoes = 0

    def start(self):
        self._state = self._state.start()

    def pause(self):
        self._state = self._state.pause()

    def reset(self):
        self._state = self._state.reset()

    def reset_all(self):
        pass

    def update(self):
        if self._state.done:
            self._state = self._state.next_state

    def as_text(self):
        task = TEXT[self._state.task.value]
        task1, task2, task3, task4 = "", "", "", ""
        if task:
            task1, task2, task3, task4 = task.splitlines()

        sets = self.tomatoes // TOMATOES_PER_SET
        if sets == 1:
            sets = "1 set completed"
        elif sets >= 2:
            sets = str(sets) + " sets completed"
        else:
            sets = ""

        return self._template.format(
            task1=task1,
            task2=task2,
            task3=task3,
            task4=task4,
            status=TEXT[self._state.status.value],
            time=self._state.time_remaining,
            count=("(`) " * (TOMATOES_PER_SET - self.tomatoes % TOMATOES_PER_SET)),
            sets=sets,
        )
