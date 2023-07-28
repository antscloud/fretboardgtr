from fretboardgtr.notes_creators import ChordFromName, ScaleFromName


def test_scale_creator():
    scale = ScaleFromName(root="C", mode="Ionian").get()
    assert scale.notes == ["C", "D", "E", "F", "G", "A", "B"]


def test_chord_creator():
    chord = ChordFromName(root="C", quality="M").get()
    assert chord.notes == ["C", "E", "G"]


def test_chord_creator_fingerings():
    fingerings = (
        ChordFromName(root="C", quality="M")
        .get()
        .get_probablely_possible_fingering(["E", "A", "D", "G", "B", "E"])
    )
    assert len(fingerings) > 1000
