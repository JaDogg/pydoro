from codecs import open
from inspect import getsource
from os.path import abspath, dirname, join

from setuptools import setup, find_packages

here = abspath(dirname(getsource(lambda: 0)))

with open(join(here, "README.rst"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="pydoro",
    version="0.1.4",
    # Get the description from second line & remove `*` character
    description=long_description.splitlines()[2][1:-1],
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/JaDogg/pydoro",
    author="Bhathiya Perera",
    author_email="jadogg.coder@gmail.com",
    python_requires=">=3.6",
    license="MIT",
    package_data={"": ["*.rst", "*.wav"]},
    install_requires=["prompt-toolkit>=3.0.2"],
    extras_require={
        'audio:platform_system=="Darwin"': [
            "pyobjc-core>=5.2",
            "pyobjc-framework-Cocoa>=5.2",
        ],
        'audio:platform_system=="Linux"': ["pycairo>=1.18.1", "PyGObject>=3.32.1"],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    keywords="tomato pomodoro pydoro timer work",
    packages=find_packages(),
    entry_points={"console_scripts": ["pydoro = pydoro.pydoro_tui:main"]},
    setup_requires=["wheel"],
)
