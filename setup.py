#!/usr/bin/env python

from setuptools import setup


description = "PyQt5 vstruct hex viewer widget."
setup(name="python-pyqt5-vstructui",
      version="0.4.0",
      description=description,
      long_description=description,
      author="Willi Ballenthin",
      author_email="willi.ballenthin@gmail.com",
      url="https://github.com/williballenthin/python-pyqt5-vstructui",
      license="Apache 2.0 License",
      install_requires=["vivisect-vstruct-wb", "python-pyqt5-hexview"],
      packages=["vstructui"],
      package_dir={"vstructui": "vstructui"},
      package_data={"vstructui": [
          "vstructui.ui",
          "defs/*.py",
      ]},
      entry_points={
        "console_scripts": [
            "vstructui=vstructui.scripts.vstructui_bin:main",
        ]
      },
)
