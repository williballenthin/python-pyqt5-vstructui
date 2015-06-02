#!/usr/bin/env python

from vstructui import __version__
from setuptools import setup


description = "PyQt5 vstruct hex viewer widget."
setup(name="python-pyqt5-vstructui",
      version=__version__,
      description=description,
      long_description=description,
      author="Willi Ballenthin",
      author_email="willi.ballenthin@gmail.com",
      url="https://github.com/williballenthin/python-pyqt5-vstructui",
      license="Apache 2.0 License",
      packages=["vstructui"])