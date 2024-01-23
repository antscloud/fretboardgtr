from fretboardgtr import FretBoard
from fretboardgtr.notes_creators import ScaleFromName

TUNING = ["E", "A", "D", "G", "B", "E"]
config = {
    "general": {
        "first_fret": 0,
        "last_fret": 16,
        "fret_width": 50,
        "show_note_name": True,
        "show_degree_name": False,
    }
}
fretboard = FretBoard(config=config)
c_scale = ScaleFromName(root="C", mode="Ionian").build().get_scale(TUNING)
c_scale[-1] = []
fretboard.add_scale(c_scale, root="C")
fretboard.export("c_scale.svg", format="svg")
