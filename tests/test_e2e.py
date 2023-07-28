import os
from pathlib import Path

from fretboardgtr.fretboard import FretBoard, FretBoardConfig
from fretboardgtr.notes_creators import ScaleFromName

C_IONIAN_SVG = Path(__file__).parent / "data" / "c_ionian.svg"
OUTPUTS_ARTIFACT_FOLDER = Path(__file__).parent / "data" / "outputs" / "e2e"


def remove_test_file(path: Path):
    if path.exists():
        os.remove(str(path))


def test_c_major_fretboard():
    fretboard = FretBoard()
    c_major = ScaleFromName(root="C", mode="Ionian").get()
    fretboard.add_notes(scale=c_major)
    os.makedirs(OUTPUTS_ARTIFACT_FOLDER, exist_ok=True)
    tmp_file = OUTPUTS_ARTIFACT_FOLDER / "horizontal.svg"
    remove_test_file(tmp_file)
    assert not tmp_file.exists()
    fretboard.export(tmp_file)
    assert tmp_file.exists()


def test_c_major_vertical_fretboard():
    fretboard = FretBoard(vertical=True)
    c_major = ScaleFromName(root="C", mode="Ionian").get()
    fretboard.add_notes(scale=c_major)
    os.makedirs(OUTPUTS_ARTIFACT_FOLDER, exist_ok=True)
    tmp_file = OUTPUTS_ARTIFACT_FOLDER / "vertical.svg"
    remove_test_file(tmp_file)
    assert not tmp_file.exists()
    fretboard.export(tmp_file)
    assert tmp_file.exists()


def test_c_major_fretboard_starting_at_5():
    config = {
        "general": {
            "first_fret": 5,
            "last_fret": 12,
        },
    }

    fretboard_config = FretBoardConfig.from_dict(config)
    fretboard = FretBoard(config=fretboard_config)
    c_major = ScaleFromName(root="C", mode="Ionian").get()
    fretboard.add_notes(scale=c_major)
    os.makedirs(OUTPUTS_ARTIFACT_FOLDER, exist_ok=True)
    tmp_file = OUTPUTS_ARTIFACT_FOLDER / "horizontal_starting_at_5.svg"
    remove_test_file(tmp_file)
    assert not tmp_file.exists()
    fretboard.export(tmp_file)
    assert tmp_file.exists()


def test_c_major_vertical_fretboard_starting_at_5():
    config = {
        "general": {
            "first_fret": 5,
            "last_fret": 12,
        },
    }

    fretboard_config = FretBoardConfig.from_dict(config)
    fretboard = FretBoard(config=fretboard_config, vertical=True)
    c_major = ScaleFromName(root="C", mode="Ionian").get()
    fretboard.add_notes(scale=c_major)
    os.makedirs(OUTPUTS_ARTIFACT_FOLDER, exist_ok=True)
    tmp_file = OUTPUTS_ARTIFACT_FOLDER / "vertical_starting_at_5.svg"
    remove_test_file(tmp_file)
    assert not tmp_file.exists()
    fretboard.export(tmp_file)
    assert tmp_file.exists()


def test_c_major_fingering():
    config = {
        "general": {
            "first_fret": 0,
            "last_fret": 5,
            "fret_width": 50,
        }
    }
    fretboard_config = FretBoardConfig.from_dict(config)
    fretboard = FretBoard(config=fretboard_config)
    c_major = [0, 3, 2, 0, 1, 0]

    fretboard.add_fingering(c_major, root="C")
    os.makedirs(OUTPUTS_ARTIFACT_FOLDER, exist_ok=True)
    tmp_file = OUTPUTS_ARTIFACT_FOLDER / "c_major_fingering.svg"
    remove_test_file(tmp_file)
    assert not tmp_file.exists()
    fretboard.export(tmp_file)
    assert tmp_file.exists()


def test_c_major_vertical_fingering():
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
    os.makedirs(OUTPUTS_ARTIFACT_FOLDER, exist_ok=True)
    tmp_file = OUTPUTS_ARTIFACT_FOLDER / "c_major_vertical_fingering.svg"
    remove_test_file(tmp_file)
    assert not tmp_file.exists()
    fretboard.export(tmp_file)
    assert tmp_file.exists()


def test_a_major_pentatonic_scale():
    config = {
        "general": {
            "first_fret": 0,
            "last_fret": 12,
            "fret_width": 50,
        }
    }
    fretboard_config = FretBoardConfig.from_dict(config)
    fretboard = FretBoard(config=fretboard_config)
    a_major_pentatonic = [[5, 8], [5, 7], [5, 7], [5, 7], [5, 8], [5, 8]]

    fretboard.add_scale(a_major_pentatonic, root="A")
    os.makedirs(OUTPUTS_ARTIFACT_FOLDER, exist_ok=True)
    tmp_file = OUTPUTS_ARTIFACT_FOLDER / "a_major_pentatonic.svg"
    remove_test_file(tmp_file)
    assert not tmp_file.exists()
    fretboard.export(tmp_file)
    assert tmp_file.exists()


def test_a_major_vertical_pentatonic_scale():
    config = {
        "general": {
            "first_fret": 0,
            "last_fret": 12,
            "fret_width": 50,
        }
    }
    fretboard_config = FretBoardConfig.from_dict(config)
    fretboard = FretBoard(config=fretboard_config, vertical=True)
    a_major_pentatonic = [[5, 8], [5, 7], [5, 7], [5, 7], [5, 8], [5, 8]]

    fretboard.add_scale(a_major_pentatonic, root="A")
    os.makedirs(OUTPUTS_ARTIFACT_FOLDER, exist_ok=True)
    tmp_file = OUTPUTS_ARTIFACT_FOLDER / "a_major_pentatonic_vertical.svg"
    remove_test_file(tmp_file)
    assert not tmp_file.exists()
    fretboard.export(tmp_file)
    assert tmp_file.exists()
