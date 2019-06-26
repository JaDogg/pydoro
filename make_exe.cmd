@echo off
pyinstaller pydoro\pydoro_tui.py --onefile --icon images\Tomato.ico --add-data ".\pydoro\pydoro_core\b15.wav;."