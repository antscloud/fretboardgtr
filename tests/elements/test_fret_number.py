from fretboardgtr.elements.fret_number import FretNumber, FretNumberConfig


def test_fret_number_get_svg():
    fret_number = FretNumber("test", position=(0.0, 0.0))
    attribs = fret_number.get_svg().attribs
    assert float(attribs["x"]) == 0.0
    assert float(attribs["y"]) == 0.0


def test_fret_number_get_svg_custom_config():
    fret_number_config = FretNumberConfig(fontsize=30)
    fret_number = FretNumber("test", position=(0.0, 0.0), config=fret_number_config)
    attribs = fret_number.get_svg().attribs
    assert fret_number.get_svg().text == "test"
    assert float(attribs["x"]) == 0.0
    assert float(attribs["y"]) == 0.0
    assert attribs["font-size"] == 30
