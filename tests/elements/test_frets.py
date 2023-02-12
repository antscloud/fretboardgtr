from fretboardgtr.elements.frets import Fret, FretConfig


def test_fret_get_svg():
    fret = Fret(start_position=(0.0, 0.0), end_position=(10.0, 10.0))
    attribs = fret.get_svg().attribs
    print(attribs)
    assert attribs["x1"] == 0.0
    assert attribs["y1"] == 0.0
    assert attribs["x2"] == 10.0
    assert attribs["y2"] == 10.0


def test_fret_get_svg_custom_config():
    fret_config = FretConfig(color="blue")
    fret = Fret(start_position=(0.0, 0.0), end_position=(10.0, 10.0), config=fret_config)
    attribs = fret.get_svg().attribs
    assert attribs["x1"] == 0.0
    assert attribs["y1"] == 0.0
    assert attribs["x2"] == 10.0
    assert attribs["y2"] == 10.0
    assert attribs["stroke"] == "blue"
