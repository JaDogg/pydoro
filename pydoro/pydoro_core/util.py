import os
import time
import sys
import subprocess


def every(delay, task):
    next_time = time.time() + delay
    while True:
        time.sleep(max(0, next_time - time.time()))
        task()
        next_time += (time.time() - next_time) // delay * delay + delay


def in_app_path(path):
    try:
        if hasattr(sys, '_MEIPASS'):
            wd = sys._MEIPASS
        else:
            wd = os.path.dirname(__file__)
        return os.path.abspath(os.path.join(wd, path))
    except AttributeError:
        return _from_resource(path)

def _from_resource(path):
    from pkg_resources import resource_filename

    res_path = resource_filename(__name__, path)
    if not os.path.exists(res_path):
        res_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    return res_path

def open_file_in_default_editor(file_path):
    '''Opens config file in another process using default editor'''
    try:
        if sys.platform.startswith('linux') or sys.platform.startswith('darwin'):
            # Unix, Linux, macOS
            editor = os.environ.get('EDITOR', 'nano')  # Use EDITOR env if available, else default to nano
            process = subprocess.Popen([editor, file_path])
        elif sys.platform.startswith('win32'):
            # Windows
            process = subprocess.Popen(['cmd', '/c', 'start', '/wait', file_path], shell=True)
        else:
            print(f"Platform {sys.platform} not supported")
            return
        # wait for editor to close
        process.wait()

    except Exception as e:
        print(f"Failed to open file: {e}")

