# FretBoardGtr

Package that make easy creation of **highly customizable** fretboards and chords diagrams

<p align="center">
    <a href="https://github.com/antscloud/fretboardgtr/actions"><img alt="CI Status" src="https://github.com/antscloud/fretboardgtr/actions/workflows/ci.yaml/badge.svg?branch=main"></a>
    <a href="https://fretboardgtr.readthedocs.io/en/latest"><img alt="Documentation Status" src="https://readthedocs.org/projects/fretboardgtr/badge/?version=latest"></a>
    <a href="https://pypi.org/project/fretboardgtr"><img alt="PyPI" src="https://img.shields.io/pypi/v/fretboardgtr.svg"></a>
    <a href="https://github.com/antscloud/fretboardgtr"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
    <a href="https://codecov.io/gh/antscloud/fretboardgtr"><img alt="Coverage Status" src="https://codecov.io/gh/antscloud/fretboardgtr/branch/main/graph/badge.svg"></a>
    <a href="https://www.gnu.org/licenses/agpl-3.0"><img alt="License: GNU Affero General Public License v3.0" src="https://img.shields.io/badge/License-AGPL_v3-blue.svg"></a>
    <a href="https://github.com/antscloud/fretboardgtr/issues"><img alt="Issue Badge" src="https://img.shields.io/github/issues/antscloud/fretboardgtr"></a>
    <a href="https://github.com/antscloud/fretboardgtr/pulls"><img alt="Pull requests Badge" src="https://img.shields.io/github/issues-pr/antscloud/fretboardgtr"></a>
</p>

- License: GNU Affero General Public License v3.0
- Documentation: https://fretboardgtr.readthedocs.io/en/latest.

## How to install 

```shell
pip install fretboardgtr
```

# Get started

```python
from fretboardgtr import FretBoard, ScaleFromName

fretboard = FretBoard()
fretboard.init_fretboard()

c_major = ScaleFromName(root="C", mode="Ionian").get()
fretboard.add_scale(c_major)

SVGExporter(fretboard.drawing).export("my_fretboard.svg")
```

## Customization example
```python
from fretboardgtr import FretBoard, ScaleFromName
config = {
    "main": {
        "first_fret": 0,
        "last_fret": 12,
        "show_tuning": False,
        "show_frets": True,
        "show_note_name": True,
        "open_color_scale": False,
        "fretted_color_scale": True,
        "open_colors": {
            "majorthird": "rgb(0, 108, 0)",
        },
        "fretted_colors": {
            "majorsixth": "rgb(222, 81, 108)",
        },
        "enharmonic": True,
    },
    "background": {"color": "rgb(150,150,150)", "opacity": 0.2},
    "fretnumber": {"color": "rgb(150,150,150)", "fontsize": 20, "fontweight": "bold"},
    "tuning": {
        "color": "rgb(150,150,150)",
        "fontsize": 20,
        "fontweight": "normal",
    },
    "string": {"color": "rgb(0,0,0)", "width": 3},
}

fretboard = FretBoard(config=config)
fretboard.init_fretboard()

c_major = ScaleFromName(root="C", mode="Ionian").get()
fretboard.add_scale(c_major)

SVGExporter(fretboard.drawing).export("my_fretboard.svg")
```

All the configuration can be found in the [documentation](https://fretboardgtr.readthedocs.io/en/latest)
