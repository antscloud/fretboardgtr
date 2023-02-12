import pytest
from fretboardgtr.fretboard import FretBoard, FretBoardConfig, FretBoardMainConfig
from fretboardgtr.elements.background import Background, BackgroundConfig
from fretboardgtr.elements.fret_number import FretNumber, FretNumberConfig
from fretboardgtr.elements.neck_dots import NeckDot, NeckDotConfig
from fretboardgtr.elements.frets import Fret, FretConfig
from fretboardgtr.elements.notes import (
    OpenNote,
    FrettedNote,
    OpenNoteConfig,
    FrettedNoteConfig,
)
from fretboardgtr.note_colors import NoteColors
from fretboardgtr.elements.nut import Nut, NutConfig
from fretboardgtr.elements.tuning import Tuning, TuningConfig
from fretboardgtr.elements.strings import String, StringConfig
from fretboardgtr.fretboard import FretBoard, FretBoardConfig, FretBoardMainConfig
from fretboardgtr.notes_creators import NotesContainer
import svgwrite
from fretboardgtr.notes_creators import ScaleFromName, ChordFromName
from fretboardgtr.exporters import SVGExporter, PNGExporter, PDFExporter
import tempfile
from pathlib import Path

C_IONIAN_SVG = Path(__file__).parent / "data" / "c_ionian.svg"


def test_c_major_fretboard():
    fretboard = FretBoard()
    fretboard.init_fretboard()
    c_major = ScaleFromName(root="C", mode="Ionian").get()
    fretboard.add_scale(c_major)
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_file = Path(tmp_dir) / "tmp.svg"
        SVGExporter(fretboard.drawing).export(tmp_file)
        with open(tmp_file, "r") as f:
            new_content = f.readlines()
        with open(C_IONIAN_SVG, "r") as f:
            test_content = f.readlines()
        assert new_content == test_content
