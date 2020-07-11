"""
This file was copied from
https://github.com/TaylorSMarks/playsound
playsound.py - For playing audio file, Copyright (c) 2016 Taylor Marks
MIT License
----
I've added async play for linux using a thread, changed names to be more pythonic
I've also added a thin wrapper around pygame as well
"""

from platform import system

system = system()


class PlayException(Exception):
    pass


def _play_sound_win(sound, block=True):
    """
    Utilizes windll.winmm. Tested and known to work with MP3 and WAVE on
    Windows 7 with Python 2.7. Probably works with more file formats.
    Probably works on Windows XP thru Windows 10. Probably works with all
    versions of Python.
    Inspired by (but not copied from) Michael Gundlach <gundlach@gmail.com>'s mp3play:
    https://github.com/michaelgundlach/mp3play
    I never would have tried using windll.winmm without seeing his code.
    """
    from ctypes import c_buffer, windll
    from random import random
    from time import sleep
    from sys import getfilesystemencoding

    def win_cmd(*command):
        buf = c_buffer(255)
        command = " ".join(command).encode(getfilesystemencoding())
        err_code = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
        if err_code:
            error_buffer = c_buffer(255)
            windll.winmm.mciGetErrorStringA(err_code, error_buffer, 254)
            exception_message = (
                "\n    Error " + str(err_code) + " for command:"
                "\n        " + command.decode() + "\n    " + error_buffer.value.decode()
            )
            raise PlayException(exception_message)
        return buf.value

    alias = "playsound_" + str(random())
    win_cmd('open "' + sound + '" alias', alias)
    win_cmd("set", alias, "time format milliseconds")
    duration_ms = win_cmd("status", alias, "length")
    win_cmd("play", alias, "from 0 to", duration_ms.decode())

    if block:
        sleep(float(duration_ms) / 1000.0)


def _play_sound_osx(sound, block=True):
    """
    Utilizes AppKit.NSSound. Tested and known to work with MP3 and WAVE on
    OS X 10.11 with Python 2.7. Probably works with anything QuickTime supports.
    Probably works on OS X 10.5 and newer. Probably works with all versions of
    Python.
    Inspired by (but not copied from) Aaron's Stack Overflow answer here:
    http://stackoverflow.com/a/34568298/901641
    I never would have tried using AppKit.NSSound without seeing his code.
    """
    from AppKit import NSSound
    from Foundation import NSURL
    from time import sleep

    if "://" not in sound:
        if not sound.startswith("/"):
            from os import getcwd

            sound = getcwd() + "/" + sound
        sound = "file://" + sound
    url = NSURL.URLWithString_(sound)
    nssound = NSSound.alloc().initWithContentsOfURL_byReference_(url, True)
    if not nssound:
        raise IOError("Unable to load sound named: " + sound)
    nssound.play()

    if block:
        sleep(nssound.duration())


def _play_sound_nix_blocking(sound):
    """Play a sound using GStreamer.
    Inspired by this:
    https://gstreamer.freedesktop.org/documentation/tutorials/playback/playbin-usage.html
    """
    # pathname2url escapes non-URL-safe characters
    import os

    try:
        from urllib.request import pathname2url
    except ImportError:
        # python 2
        from urllib import pathname2url

    import gi

    gi.require_version("Gst", "1.0")
    from gi.repository import Gst

    Gst.init(None)

    playbin = Gst.ElementFactory.make("playbin", "playbin")
    if sound.startswith(("http://", "https://")):
        playbin.props.uri = sound
    else:
        playbin.props.uri = "file://" + pathname2url(os.path.abspath(sound))

    set_result = playbin.set_state(Gst.State.PLAYING)
    if set_result != Gst.StateChangeReturn.ASYNC:
        raise PlayException("playbin.set_state returned " + repr(set_result))

    bus = playbin.get_bus()
    bus.poll(Gst.MessageType.EOS, Gst.CLOCK_TIME_NONE)
    playbin.set_state(Gst.State.NULL)


def _play_sound_nix_no_except(sound):
    # noinspection PyBroadException
    try:
        _play_sound_nix(sound)
    except:
        pass


def _play_sound_nix(sound, block=True):
    if block:
        _play_sound_nix_blocking(sound)
        return

    from threading import Thread

    thread = Thread(target=_play_sound_nix_no_except, args=(sound,), daemon=True)
    thread.start()


def _play_sound_pygame_blocking(sound):
    from pygame import mixer
    import time

    mixer.init()
    mixer.music.load(sound)
    mixer.music.play()

    while mixer.music.get_busy():
        time.sleep(0.1)


def _play_sound_pygame(sound, block=True):
    if block:
        _play_sound_pygame_blocking(sound)
        return

    from threading import Thread

    thread = Thread(target=_play_sound_pygame_blocking, args=(sound,), daemon=True)
    thread.start()


if system == "Windows":
    play = _play_sound_win
elif system == "Darwin":
    play = _play_sound_osx
else:
    # For linux this will try following libraries
    # 1) if pygame can be imported use it
    # 2) if pygame cannot be imported use PyGObject
    try:
        import pygame as try_pygame

        play = _play_sound_pygame
        del try_pygame
    except ImportError:
        play = _play_sound_nix

del system
