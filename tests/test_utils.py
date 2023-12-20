from fretboardgtr.utils import (
    _contains_duplicates,
    chromatic_position_from_root,
    chromatics_from_root,
    note_to_interval,
    note_to_interval_name,
    resolve_high_alterations_in_scale,
    scale_to_enharmonic,
    scale_to_flat,
    scale_to_intervals,
    scale_to_sharp,
    sort_scale,
    to_flat_note,
    to_sharp_note,
)


def test_contains_duplicates_false():
    elements = ["a", "b", "c"]
    assert _contains_duplicates(elements) is False


def test_contains_duplicates_true():
    elements = ["a", "b", "c", "a"]
    assert _contains_duplicates(elements) is True


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


def test_resolve_high_alterations_in_scale():
    scale = [
        "A",
        "Ab",
        "Abb",
        "A#",
        "A##",
    ]
    assert [
        "A",
        "Ab",
        "G",
        "A#",
        "B",
    ] == resolve_high_alterations_in_scale(scale)
    scale = ["A############"]
    assert [
        "A",
    ] == resolve_high_alterations_in_scale(scale)


def test_sort_scale():
    scale = [
        "C",
        "D",
        "G",
        "C#",
        "Db",
        "F#",
        "A",
        "Ab",
    ]
    assert [
        "Ab",
        "A",
        "C",
        "C#",
        "Db",
        "D",
        "F#",
        "G",
    ] == sort_scale(scale)


def test_scale_to_enharmonic():
    scale = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "Gb",
        "G",
    ]
    assert ["A", "B", "C", "D", "E", "F#", "G"] == scale_to_enharmonic(scale)
    scale = ["A#", "C", "D", "D#", "F", "G", "A"]
    assert [
        "A",
        "Bb",
        "C",
        "D",
        "Eb",
        "F",
        "G",
    ] == scale_to_enharmonic(scale)
    scale = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]
    assert [
        "A",
        "A#",
        "B",
        "C",
        "C#",
        "D",
        "D#",
        "E",
        "F",
        "F#",
        "G",
        "G#",
    ] == scale_to_enharmonic(scale)
    scale = ["F#", "G#", "A#", "B", "C#", "D#", "F"]
    assert ["Ab", "Bb", "Cb", "Db", "Eb", "F", "Gb"] == scale_to_enharmonic(scale)
    c_dorian_scale = ["C", "D", "D#", "F", "G", "A", "A#"]
    assert [
        "A",
        "Bb",
        "C",
        "D",
        "Eb",
        "F",
        "G",
    ] == scale_to_enharmonic(c_dorian_scale)
