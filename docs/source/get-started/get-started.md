# Get started

To get started simply install the package from PyPI

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

Please see the [configuration documentation](./configuration.md) for more details.
