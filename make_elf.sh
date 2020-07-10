#!/bin/bash

pyinstaller -F pydoro/pydoro_tui.py --add-data "./pydoro/pydoro_core/b15.wav:." --add-data "./.venv/Lib/site-packages/wcwidth;wcwidth" --hidden-import="pkg_resources.py2_warn"

