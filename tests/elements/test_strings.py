from fretboardgtr.elements.strings import String, StringConfig


def test_string_get_svg():
    string = String(start_position=(0.0, 0.0), end_position=(10.0, 10.0))
    attribs = string.get_svg().attribs
    print(attribs)
    assert attribs["x1"] == 0.0
    assert attribs["y1"] == 0.0
    assert attribs["x2"] == 10.0
    assert attribs["y2"] == 10.0


def test_string_get_svg_custom_config():
    string_config = StringConfig(color="blue")
    string = String(start_position=(0.0, 0.0), end_position=(10.0, 10.0), config=string_config)
    attribs = string.get_svg().attribs
    assert attribs["x1"] == 0.0
    assert attribs["y1"] == 0.0
    assert attribs["x2"] == 10.0
    assert attribs["y2"] == 10.0
    assert attribs["stroke"] == "blue"
