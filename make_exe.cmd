@echo off
pyinstaller pydoro\pydoro_tui.py -n pydoro --onefile --icon images\Tomato.ico --add-data ".\pydoro\pydoro_core\b15.wav;." --add-data ".\.venv\Lib\site-packages\wcwidth;wcwidth" --hidden-import="pkg_resources.py2_warn"

