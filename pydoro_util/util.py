import time
import os


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


def in_app_path(path):
    from pkg_resources import resource_string
    res_path = resource_string(__name__, path)

    if not os.path.exists(res_path):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)

    return res_path