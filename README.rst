Pydoro Documentation
====================

.. image:: https://github.com/JaDogg/pydoro/raw/develop/images/logo.png

.. Repo Badges

.. image:: https://badge.fury.io/py/pydoro.svg
    :alt: PyPI
    :target: https://badge.fury.io/py/pydoro
.. image:: https://github.com/JaDogg/pydoro/workflows/Python%20application/badge.svg
    :alt: CI
    :target: https://github.com/JaDogg/pydoro/actions?query=workflow%3A%22Python+application%22
.. image:: https://img.shields.io/badge/python-3.6+-blue.svg
    :alt: Python Support
    :target: https://pypi.org/project/pydoro/
.. image:: https://badges.gitter.im/pydoro/community.svg
    :alt: Chat
    :target: https://gitter.im/pydoro/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/psf/black

Introduction
============

Pydoro is a lightweight, terminal-based Pomodoro timer written in Python. It allows users to implement the Pomodoro technique without relying on mobile or web applications. The tool is privacy-friendly, does not track or store user data, and is designed for efficiency within the terminal environment.

---

Installation
============

## Install via pip:
```sh
pip install pydoro
pydoro
Install via snap (Linux):
sh
Copy
Edit
sudo snap install pydoro
pydoro
Note: Pop!_OS users need to disable sound using the following command:

sh
Copy
Edit
pydoro --no-sound
The Snap package is maintained by James Tigert (kz6fittycent).

Installing with Audio Dependencies
For audio support, use the following command:

sh
Copy
Edit
pip install "pydoro[audio]"
MacOS: Requires pyobjc-core.
Linux: Requires PyGObject.
Alternative for Linux: If PyGObject fails, try installing pygame.
Using pip3
On some systems, pip3 may be required instead of pip.

Windows Users
Windows users can try the packaged .exe file available on the releases page.

Using pipx
If you have pipx installed, run:

sh
Copy
Edit
pipx install pydoro
To inject dependencies into the pipx virtual environment:

sh
Copy
Edit
pipx inject pydoro pygame
Usage
Run pydoro to start the Pomodoro timer.

Available Options:
--no-sound : Mute alarms.
--no-clock : Hide the clock.
--focus : Disable both sound and clock.
More details are available in the wiki.

.. image:: https://github.com/JaDogg/pydoro/raw/develop/images/animation.gif

Credits
Pomodoro Technique - Invented by Francesco Cirillo.
playsound.py - Audio playback library by Taylor Marks.
prompt-toolkit - Provides terminal UI.
b15.wav - Sound by Dana Robinson (CC0 from freesound.org).
Contributors
Gabriel Cruz (gmelodie)
Zach Nelson (requiem)
Kajpio
Manuel Gutierrez (xr09)
kiba (islander)
Beatriz Uezu (beatrizuezu)
Zlatan (zlatsic)
Karolis Mažukna (nikamura)
AKeerio (akeerio)
Rohn Chatterjee (liupold)
James Tigert (kz6fittycent)
Kana
Why Pydoro?
Implements the Pomodoro Technique.
No need for mobile or web apps.
Respects privacy—no data tracking.
Optimized for terminal users.
Fully written in Python. 🐍
License
This software is Copyright (c) 2021 - 2025 Bhathiya Perera.
For more details, see the LICENSE file.

javascript
Copy
Edit

This version adjusts the structure of the original Markdown to reStructuredText (`.rst`) format. The images and badges are formatted with `.. image::`, and sections are structured with appropriate headers using `=`, `-`, or `^`.






