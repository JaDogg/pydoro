#!/bin/bash

pyinstaller -F pydoro/pydoro_tui.py --add-data "./pydoro/pydoro_core/b15.wav:."
