from fretboardgtr.elements.tuning import Tuning, TuningConfig


def test_tuning_get_svg():
    tuning = Tuning("test", position=(0.0, 0.0))
    attribs = tuning.get_svg().attribs
    assert float(attribs["x"]) == 0.0
    assert float(attribs["y"]) == 0.0


def test_tuning_get_svg_custom_config():
    tuning_config = TuningConfig(fontsize=30)
    tuning = Tuning("test", position=(0.0, 0.0), config=tuning_config)
    attribs = tuning.get_svg().attribs
    assert float(attribs["x"]) == 0.0
    assert float(attribs["y"]) == 0.0
    assert attribs["font-size"] == 30
