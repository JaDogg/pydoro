import os
import time


def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        task()
        next_time += (time.time() - next_time) // delay * delay + delay


def in_app_path(path):
    import sys

    try:
        wd = sys._MEIPASS
        return os.path.abspath(os.path.join(wd, path))
    except AttributeError:
        return _from_resource(path)


def _from_resource(path):
    from pkg_resources import resource_filename

    res_path = resource_filename(__name__, path)
    if not os.path.exists(res_path):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    return res_path
