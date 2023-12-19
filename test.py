from fretboardgtr.constants import Mode
from fretboardgtr.fretboard import FretBoard
from fretboardgtr.notes_creators import ScaleFromName

TUNING = ["E", "A", "D", "G", "B", "E"]
ROOT = "A"
MODE = Mode.MINOR_PENTATONIC

scale_positions = (
    ScaleFromName(root=ROOT, mode=MODE).get().get_scale_positions(TUNING, max_spacing=4)
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
