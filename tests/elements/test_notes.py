from fretboardgtr.elements.notes import OpenNote, OpenNoteConfig
from fretboardgtr.elements.notes import FrettedNote, FrettedNoteConfig


def test_open_note_get_svg():
    open_note = OpenNote(name="test", position=(0.0, 0.0))
    circle = open_note.get_svg().elements[0]
    text = open_note.get_svg().elements[1]
    circle_attribs = circle.attribs
    assert circle_attribs["cx"] == 0.0
    assert circle_attribs["cy"] == 0.0

    assert text.text == "test"
    text_attribs = text.attribs
    assert float(text_attribs["x"]) == 0.0
    assert float(text_attribs["y"]) == 0.0


def test_open_note_get_svg_custom_config():
    open_note_config = OpenNoteConfig(radius=30)
    open_note = OpenNote(name="test", position=(0.0, 0.0), config=open_note_config)
    circle = open_note.get_svg().elements[0]
    text = open_note.get_svg().elements[1]
    circle_attribs = circle.attribs
    assert circle_attribs["cx"] == 0.0
    assert circle_attribs["cy"] == 0.0
    assert circle_attribs["r"] == 30

    assert text.text == "test"
    text_attribs = text.attribs
    assert float(text_attribs["x"]) == 0.0
    assert float(text_attribs["y"]) == 0.0


def test_fretted_note_get_svg():
    fretted_note = FrettedNote(name="test", position=(0.0, 0.0))
    circle = fretted_note.get_svg().elements[0]
    text = fretted_note.get_svg().elements[1]
    circle_attribs = circle.attribs
    assert circle_attribs["cx"] == 0.0
    assert circle_attribs["cy"] == 0.0

    assert text.text == "test"
    text_attribs = text.attribs
    assert float(text_attribs["x"]) == 0.0
    assert float(text_attribs["y"]) == 0.0


def test_fretted_note_get_svg_custom_config():
    fretted_note_config = FrettedNoteConfig(radius=30)
    fretted_note = FrettedNote(name="test", position=(0.0, 0.0), config=fretted_note_config)
    circle = fretted_note.get_svg().elements[0]
    text = fretted_note.get_svg().elements[1]
    circle_attribs = circle.attribs
    assert circle_attribs["cx"] == 0.0
    assert circle_attribs["cy"] == 0.0
    assert circle_attribs["r"] == 30

    assert text.text == "test"
    text_attribs = text.attribs
    assert float(text_attribs["x"]) == 0.0
    assert float(text_attribs["y"]) == 0.0
