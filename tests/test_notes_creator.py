import pytest
from fretboardgtr.notes_creators import ScaleFromName, ChordFromName


def test_scale_creator():
    scale = ScaleFromName(root="C", mode="Ionian").get()
    print(scale.notes)
    assert scale.notes == ["C", "D", "E", "F", "G", "A", "B"]


def test_chord_creator():
    chord = ChordFromName(root="C", quality="M").get()
    assert chord.notes == ["C", "E", "G"]
