# Get started

To get started simply install the package from PyPI

## How to install

`fretboardgtr` needs to have the following install in order to run :

```shell
sudo apt install libcairo2-dev pkg-config
```

```shell
pip install fretboardgtr
```

## Usage

```python
from fretboardgtr.fretboard import FretBoard
from fretboardgtr.notes_creators import ScaleFromName

fretboard = FretBoard()
c_major = ScaleFromName(root="C", mode="Ionian").build()
fretboard.add_notes(scale=c_major)
fretboard.export("my_fretboard.svg", format="svg")
```

![My Fretboard](../assets/my_fretboard.svg)
## Customization example

```python
from fretboardgtr.fretboard import FretBoard, FretBoardConfig
from fretboardgtr.notes_creators import ScaleFromName

config = {
    "general": {
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
c_major = ScaleFromName(root="A", mode="Ionian").build()
fretboard.add_notes(scale=c_major)
fretboard.export("my_custom_fretboard.svg", format="svg")
```


![My custom Fretboard](../assets/my_custom_fretboard.svg)
Please see the [configuration documentation](./configuration.md) for more details.


## Vertical Fretboard
```python
from fretboardgtr.fretboard import FretBoard
from fretboardgtr.notes_creators import ScaleFromName

fretboard = FretBoard(vertical=True)
c_major = ScaleFromName(root="C", mode="Ionian").build()
fretboard.add_notes(scale=c_major)
fretboard.export("my_vertical_fretboard.svg", format="svg")
```

```{image} ../assets/my_vertical_fretboard.svg
:alt: My vertical fretboard
:width: 200px
:align: center
```
## Examples

### Draw a chord diagram

```python
from fretboardgtr.fretboard import FretBoardConfig, FretBoard

config = {
    "general": {
        "first_fret": 0,
        "last_fret": 5,
        "fret_width": 50,
    }
}
fretboard_config = FretBoardConfig.from_dict(config)
fretboard = FretBoard(config=fretboard_config, vertical=True)
c_major = [0, 3, 2, 0, 1, 0]

fretboard.add_fingering(c_major, root="C")
fretboard.export("my_vertical_fretboard.svg", format="svg")
```

```{image} ../assets/c_major_chord.svg
:alt: My vertical fretboard
:width: 200px
:align: center
```

### Draw all propably possible chord position for a specific chord

⚠️ Be careful with this snippets. This example generates over 1000 svgs
```python
from fretboardgtr.fretboard import FretBoardConfig, FretBoard
from fretboardgtr.constants import Chord
from fretboardgtr.notes_creators import ChordFromName

TUNING = ["E", "A", "D", "G", "B", "E"]
ROOT = "C"
QUALITY = Chord.MAJOR

fingerings = (
    ChordFromName(root=ROOT, quality=QUALITY).build().get_chord_fingerings(TUNING)
)
for i, fingering in enumerate(fingerings):
    _cleaned_fingering = [pos for pos in fingering if pos is not None and pos != 0]
    first_fret = min(_cleaned_fingering) - 2
    if first_fret < 0:
        first_fret = 0

    last_fret = max(_cleaned_fingering) + 2
    if last_fret < 4:
        last_fret = 4

    config = {
        "general": {
            "first_fret": first_fret,
            "last_fret": last_fret,
            "fret_width": 50,
        }
    }
    fretboard_config = FretBoardConfig.from_dict(config)
    fretboard = FretBoard(config=fretboard_config, tuning=TUNING, vertical=True)
    fretboard.add_fingering(fingering, root=ROOT)
    fretboard.export(
        f"./{ROOT}_{QUALITY.value}/{ROOT}_{QUALITY.value}_position_{i}.svg",
        format="svg",
    )


```

Will give you :

```{image} ../assets/C_M/C_M_position_0.svg
:alt: My vertical fretboard
:width: 200px
:align: center
```


```{image} ../assets/C_M/C_M_position_1.svg
:alt: My vertical fretboard
:width: 200px
:align: center
```


```{image} ../assets/C_M/C_M_position_2.svg
:alt: My vertical fretboard
:width: 200px
:align: center
```

```{image} ../assets/C_M/C_M_position_3.svg
:alt: My vertical fretboard
:width: 200px
:align: center
```
And so on.

### Generate all the classic positions for A minor pentatonic scale

```python
from fretboardgtr.fretboard import FretBoardConfig, FretBoard
from fretboardgtr.notes_creators import ScaleFromName
from fretboardgtr.constants import Mode

TUNING = ["E", "A", "D", "G", "B", "E"]
ROOT = "A"
MODE = Mode.MINOR_PENTATONIC

scale_positions = (
    ScaleFromName(root=ROOT, mode=MODE).build().get_scale_positions(TUNING, max_spacing=4)
)
config = {
    "general": {
        "last_fret": 16,
    }
}

for i, scale_position in enumerate(scale_positions):
    fretboard = FretBoard(config=config, tuning=TUNING)
    fretboard.add_scale(scale_position, root=ROOT)
    fretboard.export(
        f"./{ROOT}_{MODE.value}/{ROOT}_{MODE.value}_position_{i}.svg", format="svg"
    )
```

Will give you :

```{image} ../assets/A_Minorpentatonic/A_Minorpentatonic_position_0.svg
:alt: My vertical fretboard
:width: 80%
:align: center
```


```{image} ../assets/A_Minorpentatonic/A_Minorpentatonic_position_1.svg
:alt: My vertical fretboard
:width: 80%
:align: center
```


```{image} ../assets/A_Minorpentatonic/A_Minorpentatonic_position_2.svg
:alt: My vertical fretboard
:width: 80%
:align: center
```

And so on.
