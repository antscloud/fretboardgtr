"""The setup script."""
from typing import Dict

from setuptools import setup

version: Dict[str, str] = {}
with open("fretboardgtr/_version.py") as fp:
    exec(fp.read(), version)

setup(version=version["version_str"])
