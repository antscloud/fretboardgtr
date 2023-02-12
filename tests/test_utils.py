import pytest

from fretboardgtr.utils import (
    _contains_duplicates,
    chromatics_from_root,
    chromatic_position_from_root,
    to_sharp_note,
    to_flat_note,
    scale_to_sharp,
    scale_to_flat,
    note_to_interval,
    note_to_interval_name,
    scale_to_intervals,
    scale_to_enharmonic,
)


def test_contains_duplicates_false():
    l = ["a", "b", "c"]
    assert False == _contains_duplicates(l)


def test_contains_duplicates_true():
    l = ["a", "b", "c", "a"]
    assert True == _contains_duplicates(l)


def test_chromatics_from_root_a():
    root = "A"
    results = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    assert results == chromatics_from_root(root)


def test_chromatics_from_root_c():
    root = "C"
    results = [
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
        "A",
        "A#",
        "B",
    ]
    assert results == chromatics_from_root(root)


def test_chromatics_position_from_root():
    assert 3 == chromatic_position_from_root(root="A", note="C")
    assert 7 == chromatic_position_from_root(root="C", note="G")


def test_to_sharp_note_a():
    assert "A" == to_sharp_note("A")


def test_to_sharp_note_a_sharp():
    assert "A#" == to_sharp_note("Bb")


def test_to_flat_note_a():
    assert "A" == to_flat_note("A")


def test_to_flat_note_a_sharp():
    assert "Bb" == to_flat_note("A#")


def test_scale_to_sharp():
    scale = ["A", "Bb", "B", "C", "C#"]
    assert ["A", "A#", "B", "C", "C#"] == scale_to_sharp(scale)


def test_scale_to_flat():
    scale = ["A", "Bb", "B", "C", "C#"]
    assert ["A", "Bb", "B", "C", "Db"] == scale_to_flat(scale)


def test_note_to_interval():
    root = "C"
    note = "G"
    assert 7 == note_to_interval(note, root)


def test_note_to_interval_name():
    root = "C"
    note = "G"
    assert "5" == note_to_interval_name(note, root)


def test_scale_to_intervals():
    scale = ["C", "E", "G"]
    assert [0, 4, 7] == scale_to_intervals(scale, root="C")


def test_scale_to_enharmonic():
    scale = ["G", "A", "B", "C", "D", "E", "Gb"]
    assert ["G", "A", "B", "C", "D", "E", "F#"] == scale_to_enharmonic(scale)