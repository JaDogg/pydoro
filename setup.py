from codecs import open
from inspect import getsource
from os.path import abspath, dirname, join
from platform import system

from setuptools import setup, find_packages

here = abspath(dirname(getsource(lambda: 0)))
system = system()

with open(join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

requires = ["prompt-toolkit>=2.0.9"]
# WHY:
# On OSX we need pyobjc to actually play a sound
if system == "Darwin":
    requires.extend(["pyobjc-core>=5.2", "pyobjc-framework-Cocoa>=5.2"])

setup(
    name="pydoro",
    version="0.1.0",
    description=long_description.splitlines()[2][1:-1],
    long_description=long_description,
    url="https://github.com/JaDogg/pydoro",
    author="Bhathiya Perera",
    author_email="jadogg.coder@gmail.com",
    license="MIT",
    scripts=["pydoro.py"],
    package_data={"": ["*.rst"], "pydoro_util": ["b15.wav"]},
    install_requires=requires,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
    keywords="tomato pomodoro pydoro timer work",
    packages=find_packages(),
)
