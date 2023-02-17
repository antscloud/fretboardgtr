# FretBoardGtr

Package that make easy creation of **highly customizable** fretboards and chords diagrams

<p align="center">
    <a href="https://github.com/antscloud/fretboardgtr/actions"><img alt="CI Status" src="https://github.com/antscloud/fretboardgtr/actions/workflows/ci.yaml/badge.svg?branch=master"></a>
    <a href="https://fretboardgtr.readthedocs.io/en/latest"><img alt="Documentation Status" src="https://readthedocs.org/projects/fretboardgtr/badge/?version=latest"></a>
    <a href="https://pypi.org/project/fretboardgtr"><img alt="PyPI" src="https://img.shields.io/pypi/v/fretboardgtr.svg"></a>
    <a href="https://github.com/antscloud/fretboardgtr"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    <a href="https://codecov.io/gh/antscloud/fretboardgtr"><img alt="Coverage Status" src="https://codecov.io/gh/antscloud/fretboardgtr/branch/master/graph/badge.svg"></a>
    <a href="https://www.gnu.org/licenses/agpl-3.0"><img alt="License: GNU Affero General Public License v3.0" src="https://img.shields.io/badge/License-AGPL_v3-blue.svg"></a>
    <a href="https://github.com/antscloud/fretboardgtr/issues"><img alt="Issue Badge" src="https://img.shields.io/github/issues/antscloud/fretboardgtr"></a>
    <a href="https://github.com/antscloud/fretboardgtr/pulls"><img alt="Pull requests Badge" src="https://img.shields.io/github/issues-pr/antscloud/fretboardgtr"></a>
</p>

- License: GNU Affero General Public License v3.0
- Documentation: https://fretboardgtr.readthedocs.io/en/latest.

# Get started

To get started simply install the package from PyPI

## How to install

```shell
pip install fretboardgtr
```

## Usage

```python
from fretboardgtr.fretboard import FretBoard
from fretboardgtr.notes_creators import ScaleFromName

fretboard = FretBoard()
c_major = ScaleFromName(root="C", mode="Ionian").get()
fretboard.add_notes(scale=c_major)
fretboard.export("my_fretboard.svg", format="svg")
```

![My Fretboard](docs/source/assets/my_fretboard.svg)

## Documentation

All the documentation can be found in the [documentation](https://fretboardgtr.readthedocs.io/en/latest)
