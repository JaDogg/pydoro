pydoro 🍅
============
*Terminal Pomodoro Timer*

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

Installation 🎉
-----------------
Install via pip:

.. code-block::

    $ pip install pydoro
    $ pydoro

Install via snap (Linux):

.. code-block::

    $ sudo snap install pydoro
    $ pydoro
    
 
* NOTE: Pop!_OS users will need to run pydoro without sound, using this command option: :code:`pydoro --no-sound`
* Snap package is maintained by James Tigert ( kz6fittycent_ )

Done.

You can also use :code:`pip install "pydoro[audio]"` to get audio dependencies for OSX(:code:`pyobjc-core`) and Linux(:code:`PyGObject`).

Also for Linux :code:`pygame` will be used if it's installed. (Try this if you cannot get :code:`PyGObject` to work)

For some systems you may have to use :code:`pip3` instead. **Only Python 3.6+ is supported.**

On windows you may try the packaged .exe file. See the releases_ page.

If you have pipx:

.. code-block::

    $ pipx install pydoro
    
You can also inject dependencies to pipx virtual environment using

.. code-block::

    $ pipx inject pydoro pygame

Usage 📖
---------
* Run :code:`pydoro` to launch. More info in wiki_.

.. image:: https://github.com/JaDogg/pydoro/raw/develop/images/animation.gif

.. _wiki: https://github.com/JaDogg/pydoro/wiki


**Options:** Use `--no-sound` to mute alarms, `--no-clock` to hide the clock or `--focus` for both clock hiding and sound muting

Credits 🙇‍♂️
------------------
* Pomodoro - Invented by Francesco Cirillo
* playsound.py - For playing audio file, Copyright (c) 2016 Taylor_ Marks
* prompt-toolkit - Awesome TUI library 😎
* b15.wav - Dana_ robinson designs, CC0 from freesound

.. _releases: https://github.com/JaDogg/pydoro/releases
.. _Taylor: https://github.com/TaylorSMarks/playsound
.. _Dana: https://freesound.org/s/377639/

Contributors 🙏
------------------
* Gabriel Cruz - gmelodie_
* Zach Nelson - requiem_
* Kajpio - kajpio_
* Manuel Gutierrez - xr09_
* kiba - islander_
* Beatriz Uezu - beatrizuezu_
* Zlatan - zlatsic_
* Karolis Mažukna - nikamura_
* AKeerio - akeerio_
* Rohn Chatterjee - liupold_
* James Tigert - kz6fittycent_
* Kana - kana_

.. _gmelodie: https://github.com/gmelodie
.. _requiem: https://github.com/Requiem
.. _kajpio: https://github.com/Kajpio
.. _xr09: https://github.com/xr09
.. _islander: https://github.com/islander
.. _beatrizuezu: https://github.com/beatrizuezu
.. _zlatsic: https://github.com/ZlatSic
.. _nikamura: https://github.com/Nikamura
.. _akeerio: https://github.com/AKeerio
.. _liupold: https://github.com/liupold
.. _kz6fittycent: https://github.com/kz6fittycent
.. _kana: https://github.com/kana800

Why ? 🤔
------------
* I wanted to follow `Pomodoro Technique`_.
* I don't like to use mobile apps or web apps.
* No user info is stored, tracked or shared.
* I spend lot of time on my Terminal.
* Written in Python 🐍.

.. _Pomodoro Technique: https://en.wikipedia.org/wiki/Pomodoro_Technique


Copyright ⚖
----------------
This software is Copyright (c) 2021 - 2022 Bhathiya Perera.

See the LICENSE file for more information.
