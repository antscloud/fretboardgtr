from fretboardgtr.elements.background import Background, BackgroundConfig


def test_background_get_svg():
    background = Background(position=(0.0, 0.0), size=(10.0, 10.0))
    attribs = background.get_svg().attribs
    assert attribs["x"] == 0.0
    assert attribs["y"] == 0.0
    assert attribs["width"] == 10.0
    assert attribs["height"] == 10.0


def test_background_get_svg_custom_config():
    background_config = BackgroundConfig(color="blue")
    background = Background(position=(0.0, 0.0), size=(10.0, 10.0), config=background_config)
    attribs = background.get_svg().attribs
    assert attribs["x"] == 0.0
    assert attribs["y"] == 0.0
    assert attribs["width"] == 10.0
    assert attribs["height"] == 10.0
    assert attribs["fill"] == "blue"
