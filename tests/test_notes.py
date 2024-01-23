import pytest

from fretboardgtr.notes import Note


@pytest.mark.parametrize("invalid_note", ["Z", "H", "Invalid"])
def test_invalid_note_creation(invalid_note):
    with pytest.raises(ValueError):
        Note(invalid_note)


@pytest.mark.parametrize(
    "valid_note",
    ["C", "C#", "C###" "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"],
)
def test_valid_note_creation(valid_note):
    note = Note(valid_note)
    assert str(note) == valid_note


@pytest.mark.parametrize(
    "note_str, expected_resolved_note, prefer_flat",
    [
        ("Fb", "E", False),
        ("D#", "D#", False),
        ("Ab", "Ab", True),
        ("Abbb", "Gb", True),
        ("F#", "F#", False),
        ("E#", "F", False),
        ("G#", "G#", False),
        ("A#", "A#", False),
        ("B#", "C", False),
    ],
)
def test_resolve(note_str, expected_resolved_note, prefer_flat):
    note = Note(note_str)
    resolved_note = note.resolve(prefer_flat)
    assert str(resolved_note) == expected_resolved_note


@pytest.mark.parametrize(
    "note_str, expected_sharpened_note",
    [
        ("D", "D#"),
        ("C", "C#"),
        ("Db", "D"),
        ("Dbb", "Db"),
        ("Dbbbb", "Dbbb"),
        ("D#", "D##"),
    ],
)
def test_sharpen(note_str, expected_sharpened_note):
    note = Note(note_str)
    sharpened_note = note.sharpen()
    assert str(sharpened_note) == expected_sharpened_note


@pytest.mark.parametrize(
    "note_str, expected_flattened_note",
    [
        ("D", "Db"),
        ("C", "Cb"),
        ("Db", "Dbb"),
        ("D#", "D"),
    ],
)
def test_flatten(note_str, expected_flattened_note):
    note = Note(note_str)
    flattened_note = note.flatten()
    assert str(flattened_note) == expected_flattened_note


@pytest.mark.parametrize(
    "note_str, expected_flat_enharmonic_note",
    [
        ("A#", "Bb"),
        ("A##", "B"),
        ("A###", "C"),
        ("A####", "Db"),
        ("A", "Bbb"),
        ("Ab", "Bbbb"),
        ("G#", "Ab"),
        ("G", "Abb"),
        ("Gb", "Abbb"),
        ("F#", "Gb"),
        ("F", "Gbb"),
        ("E", "Fb"),
        ("E#", "F"),
        ("Eb", "Fbb"),
    ],
)
def test_flat_enharmonic(note_str, expected_flat_enharmonic_note):
    note = Note(note_str)
    flat_enharmonic_note = note.flat_enharmonic()
    assert str(flat_enharmonic_note) == expected_flat_enharmonic_note


@pytest.mark.parametrize(
    "note_str, expected_sharp_enharmonic_note",
    [
        ("Ab", "G#"),
        ("Abb", "G"),
        ("Abbb", "F#"),
        ("Abbbb", "F"),
        ("A", "G##"),
        ("A#", "G###"),
        ("Gb", "F#"),
        ("G", "F##"),
        ("G#", "F###"),
        ("Fb", "E"),
        ("F", "E#"),
        ("E", "D##"),
        ("Eb", "D#"),
    ],
)
def test_sharp_enharmonic(note_str, expected_sharp_enharmonic_note):
    note = Note(note_str)
    sharp_enharmonic_note = note.sharp_enharmonic()
    assert str(sharp_enharmonic_note) == expected_sharp_enharmonic_note
