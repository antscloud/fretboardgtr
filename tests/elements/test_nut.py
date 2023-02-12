from fretboardgtr.elements.nut import Nut, NutConfig


def test_nut_get_svg():
    nut = Nut(start_position=(0.0, 0.0), end_position=(10.0, 10.0))
    attribs = nut.get_svg().attribs
    print(attribs)
    assert attribs["x1"] == 0.0
    assert attribs["y1"] == 0.0
    assert attribs["x2"] == 10.0
    assert attribs["y2"] == 10.0


def test_nut_get_svg_custom_config():
    nut_config = NutConfig(color="blue")
    nut = Nut(start_position=(0.0, 0.0), end_position=(10.0, 10.0), config=nut_config)
    attribs = nut.get_svg().attribs
    assert attribs["x1"] == 0.0
    assert attribs["y1"] == 0.0
    assert attribs["x2"] == 10.0
    assert attribs["y2"] == 10.0
    assert attribs["stroke"] == "blue"
