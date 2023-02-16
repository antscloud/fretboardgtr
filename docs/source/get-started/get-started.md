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

![My Fretboard](../assets/my_fretboard.svg)
## Customization example

```python
from fretboardgtr.fretboard import FretBoard, FretBoardConfig
from fretboardgtr.notes_creators import ScaleFromName

config = {
    "main": {
        "first_fret": 0,
        "last_fret": 24,
        "show_tuning": False,
        "show_frets": True,
        "show_note_name": False,
        "show_degree_name": True,
        "open_color_scale": True,
        "fretted_color_scale": True,
        "fretted_colors": {
            "root": "rgb(255,255,255)",
        },
        "open_colors": {
            "root": "rgb(255,255,255)",
        },
        "enharmonic": True,
    },
    "background": {"color": "rgb(0,0,50)", "opacity": 0.4},
    "frets": {"color": "rgb(150,150,150)"},
    "fret_numbers": {"color": "rgb(150,150,150)", "fontsize": 20, "fontweight": "bold"},
    "strings": {"color": "rgb(200,200,200)", "width": 2},
}

fretboard_config = FretBoardConfig.from_dict(config)
fretboard = FretBoard(config=fretboard_config)
c_major = ScaleFromName(root="A", mode="Ionian").get()
fretboard.add_notes(scale=c_major)
fretboard.export("my_custom_fretboard.svg", format="svg")
```


![My custom Fretboard](../assets/my_custom_fretboard.svg)
Please see the [configuration documentation](./configuration.md) for more details.


## Vertical Fretboard
```python
from fretboardgtr.fretboard import VerticalFretBoard
from fretboardgtr.notes_creators import ScaleFromName

fretboard = VerticalFretBoard()
c_major = ScaleFromName(root="C", mode="Ionian").get()
fretboard.add_notes(scale=c_major)
fretboard.export("my_vertical_fretboard.svg", format="svg")
```

<p align="center">
  <img src="../assets/my_vertical_fretboard.svg" width="250"/>
</p>
