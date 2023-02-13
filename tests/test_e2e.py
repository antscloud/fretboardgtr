import tempfile
from pathlib import Path

from fretboardgtr.exporters import SVGExporter
from fretboardgtr.fretboard import FretBoard
from fretboardgtr.notes_creators import ScaleFromName

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
