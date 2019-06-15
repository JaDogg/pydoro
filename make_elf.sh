#!/bin/bash

pyinstaller -F pydoro/pydoro.py --add-data "./pydoro/pydoro_core/b15.wav:."
