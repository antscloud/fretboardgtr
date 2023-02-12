from fretboardgtr.elements.neck_dots import NeckDot, NeckDotConfig


def test_neck_dots_get_svg():
    neck_dot = NeckDot(position=(0.0, 0.0))
    attribs = neck_dot.get_svg().attribs
    assert attribs["cx"] == 0.0
    assert attribs["cy"] == 0.0


def test_neck_dots_get_svg_custom_config():
    neck_dot_config = NeckDotConfig(radius=30)
    neck_dot = NeckDot(position=(0.0, 0.0), config=neck_dot_config)
    attribs = neck_dot.get_svg().attribs
    assert attribs["cx"] == 0.0
    assert attribs["cy"] == 0.0
    assert attribs["r"] == 30
