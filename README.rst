pydoro 🍅
============
*Terminal Pomodoro Timer*  
Pydoro is a terminal-based Pomodoro timer designed to help you improve focus and productivity using the Pomodoro Technique. This technique breaks down work into intervals, traditionally 25 minutes of focused work followed by a short break, with longer breaks after completing a set number of intervals. Pydoro provides a simple, distraction-free interface for using this method directly in your terminal.

.. image:: https://github.com/JaDogg/pydoro/raw/develop/images/logo.png  
    :alt: Pydoro Logo  
    :description: The logo for the Pydoro project, representing the Pomodoro timer tool in a terminal environment.

Repo Badges
-----------
The following badges are displayed to give useful insights into the status of the Pydoro project:

.. image:: https://badge.fury.io/py/pydoro.svg  
    :alt: PyPI  
    :target: https://badge.fury.io/py/pydoro  
    :description: This badge shows the latest version of Pydoro available on PyPI (Python Package Index). It indicates that the package is actively maintained and easily accessible for installation via pip.

.. image:: https://github.com/JaDogg/pydoro/workflows/Python%20application/badge.svg  
    :alt: Continuous Integration Status  
    :target: https://github.com/JaDogg/pydoro/actions?query=workflow%3A%22Python+application%22  
    :description: This badge displays the build status of the latest version. It provides assurance that the code passes all tests in the CI pipeline, confirming that Pydoro is stable and functional.

.. image:: https://img.shields.io/badge/python-3.6+-blue.svg  
    :alt: Python Support  
    :target: https://pypi.org/project/pydoro/  
    :description: Indicates that Pydoro supports Python version 3.6 and above, ensuring compatibility with modern Python environments.

.. image:: https://badges.gitter.im/pydoro/community.svg  
    :alt: Community Chat  
    :target: https://gitter.im/pydoro/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge  
    :description: This badge links to the Gitter community chat where you can interact with other users and contributors to discuss features, issues, and improvements for Pydoro.

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg  
    :target: https://github.com/psf/black  
    :description: This badge indicates that the project follows the Black code style, a code formatter for Python that ensures consistent, clean, and readable code throughout the project.

Installation 🎉
--------------
Follow the instructions below to install Pydoro and get started with this Pomodoro timer.

**Install via pip (Python Package Index):**

The simplest way to install Pydoro is through pip. This method is compatible with Python 3.6+.

.. code-block::

    $ pip install pydoro
    $ pydoro

After installation, you can run Pydoro directly from the terminal using the `pydoro` command.

**Install via snap (Linux):**

If you're using a Linux system, you can also install Pydoro via Snap, which is a universal package manager:

.. code-block::

    $ sudo snap install pydoro
    $ pydoro

* **Note for Pop!_OS users:** If you're using Pop!_OS, use the `--no-sound` option when running Pydoro to avoid sound playback, as this may conflict with system settings.

**Install with Audio Dependencies (macOS/Linux):**

If you want to enable audio features (such as sound notifications) on macOS or Linux, you'll need to install the required dependencies. You can do so by running the following command:

.. code-block::

    $ pip install "pydoro[audio]"

- For **macOS**: It will install `pyobjc-core`.
- For **Linux**: It will install `PyGObject` for audio functionality.
- If you encounter issues with `PyGObject`, Pygame will be used if it is installed.

**Use pip3 (For Certain Systems):**

If your system uses `pip3` instead of `pip`, you can use the following command to install Pydoro:

.. code-block::

    $ pip3 install pydoro

**Install via pipx (Recommended for Isolated Environments):**

If you prefer to run Pydoro in an isolated environment using `pipx`, you can install it with the following command:

.. code-block::

    $ pipx install pydoro

You can also inject additional dependencies, like Pygame for sound support, into the pipx environment:

.. code-block::

    $ pipx inject pydoro pygame

Usage 📖
---------
Once installed, you can start using Pydoro directly from your terminal with the following command:

.. code-block::

    $ pydoro

This will launch the Pomodoro timer interface in your terminal.

### Available Options:

- `--no-sound`: Disables the sound notifications, allowing for a quieter experience.
- `--no-clock`: Hides the Pomodoro clock display during the timer countdown.
- `--focus`: Hides the clock and disables sound to help you focus fully during the Pomodoro session.

For a more in-depth look at the features, refer to the [Pydoro Wiki](https://github.com/JaDogg/pydoro/wiki).

A demonstration of Pydoro in action:

.. image:: https://github.com/JaDogg/pydoro/raw/develop/images/animation.gif  
    :alt: Pydoro in Action  
    :description: Watch Pydoro in action as it runs through a typical Pomodoro session.

Credits 🙇‍♂️
------------
Pydoro has benefited from the contributions of various individuals and libraries. Here's a list of the notable contributors and resources:

- **Pomodoro Technique**: The Pomodoro Technique, developed by Francesco Cirillo, is the core concept behind Pydoro. It involves working in short, focused intervals followed by breaks to enhance productivity.
  - Learn more about it on [Wikipedia](https://en.wikipedia.org/wiki/Pomodoro_Technique).
  
- **playsound.py**: Pydoro uses this simple Python module for playing sound notifications during Pomodoro sessions.
  - Repository: [playsound.py - Taylor Marks](https://github.com/TaylorSMarks/playsound).
  
- **prompt-toolkit**: This library is used for building interactive command-line applications, providing the UI for Pydoro in the terminal.
  - Repository: [prompt-toolkit](https://github.com/prompt-toolkit/prompt_toolkit).
  
- **b15.wav**: A sound file used for alarm notifications in Pydoro, created by Dana Robinson and released under CC0.
  - Sound file: [b15.wav - Dana Robinson](https://freesound.org/s/377639/).

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

Why? 🤔
---------
Pydoro was created with the following objectives in mind:

- **Simplification**: Provide a lightweight, terminal-based Pomodoro timer that doesn't require external applications or online tools.
- **Privacy**: Operate entirely offline, ensuring that no user data is collected or tracked.
- **Productivity**: Offer a distraction-free way to manage work intervals, helping users stay productive throughout their day.
- **Customization**: Written in Python to be easily customizable and extendable according to personal or organizational needs.

Copyright ⚖
-------------
Pydoro is released under the MIT License.  
Copyright (c) 2021 - 2025 **Bhathiya Perera**.

For licensing details, please refer to the LICENSE file.
