from typing import List

from fretboardgtr.fretboard import FretBoard, FretBoardConfig

config = {
    "general": {
        "first_fret": 0,
        "last_fret": 16,
        "fret_width": 50,
        "show_note_name": True,
        "show_degree_name": False,
    }
}
fretboard_config = FretBoardConfig.from_dict(config)
fretboard = FretBoard(config=fretboard_config, vertical=True)
c_major: List[int | None] = [0, 3, 2, 0, 1, 0]
fretboard.add_fingering(c_major, root="C")
fretboard.export("chords_fretboard.svg", format="svg")
