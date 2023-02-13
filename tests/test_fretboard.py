import pytest
import svgwrite

from fretboardgtr.elements.background import BackgroundConfig
from fretboardgtr.elements.fret_number import FretNumberConfig
from fretboardgtr.elements.frets import FretConfig
from fretboardgtr.elements.neck_dots import NeckDotConfig
from fretboardgtr.elements.notes import FrettedNoteConfig, OpenNote, OpenNoteConfig
from fretboardgtr.elements.nut import NutConfig
from fretboardgtr.elements.strings import StringConfig
from fretboardgtr.elements.tuning import TuningConfig
from fretboardgtr.fretboard import FretBoard, FretBoardConfig, FretBoardMainConfig
from fretboardgtr.note_colors import NoteColors
from fretboardgtr.notes_creators import NotesContainer


@pytest.fixture()
def default_config():
    return FretBoardConfig(
        main=FretBoardMainConfig(
            x_start=30.0,
            y_start=30.0,
            fret_height=50,
            fret_width=70,
            first_fret=0,
            last_fret=12,
            show_tuning=True,
            show_frets=True,
            show_nut=True,
            show_degree_name=False,
            show_note_name=True,
            open_color_scale=False,
            fretted_color_scale=True,
            open_colors=NoteColors(
                root="rgb(231, 0, 0)",
                minorsecond="rgb(249, 229, 0)",
                majorsecond="rgb(249, 165, 0)",
                minorthird="rgb(0, 94, 0)",
                majorthird="rgb(0, 108, 0)",
                perfectfourth="rgb(0, 154, 0)",
                diminishedfifth="rgb(0, 15, 65)",
                perfectfifth="rgb(0, 73, 151)",
                minorsixth="rgb(168, 107, 98)",
                majorsixth="rgb(222, 81, 108)",
                minorseventh="rgb(120, 37, 134)",
                majorseventh="rgb(120, 25, 98)",
            ),
            fretted_colors=NoteColors(
                root="rgb(231, 0, 0)",
                minorsecond="rgb(249, 229, 0)",
                majorsecond="rgb(249, 165, 0)",
                minorthird="rgb(0, 94, 0)",
                majorthird="rgb(0, 108, 0)",
                perfectfourth="rgb(0, 154, 0)",
                diminishedfifth="rgb(0, 15, 65)",
                perfectfifth="rgb(0, 73, 151)",
                minorsixth="rgb(168, 107, 98)",
                majorsixth="rgb(222, 81, 108)",
                minorseventh="rgb(120, 37, 134)",
                majorseventh="rgb(120, 25, 98)",
            ),
            enharmonic=True,
        ),
        background=BackgroundConfig(color="rgb(150,150,150)", opacity=0.2),
        fretnumber=FretNumberConfig(
            color="rgb(150,150,150)", fontsize=20, fontweight="bold"
        ),
        neckdot=NeckDotConfig(
            color="rgb(200,200,200)",
            color_stroke="rgb(0,0,0)",
            width_stroke=2,
            radius=7,
        ),
        fret=FretConfig(color="rgb(150,150,150)", width=3),
        nut=NutConfig(color="rgb(0,0,0)", width=6),
        tuning=TuningConfig(
            color="rgb(150,150,150)",
            fontsize=20,
            fontweight="normal",
        ),
        string=StringConfig(color="rgb(0,0,0)", width=3),
        open_note=OpenNoteConfig(
            radius=20,
            color="rgb(255,255,255)",
            stroke_color="rgb(0,0,0)",
            stroke_width=3,
            text_color="rgb(0,0,0)",
            fontsize=20,
            fontweight="bold",
        ),
        fretted_note=FrettedNoteConfig(
            radius=20,
            color="rgb(255,255,255)",
            stroke_color="rgb(0,0,0)",
            stroke_width=3,
            text_color="rgb(0,0,0)",
            fontsize=20,
            fontweight="bold",
        ),
    )


@pytest.fixture()
def dict_config():
    return dict(
        main=dict(
            x_start=30.0,
            y_start=30.0,
            fret_height=50,
            fret_width=70,
            first_fret=0,
            last_fret=12,
            show_tuning=True,
            show_frets=True,
            show_nut=True,
            show_degree_name=False,
            show_note_name=True,
            open_color_scale=False,
            fretted_color_scale=True,
            open_colors=dict(
                root="rgb(231, 0, 0)",
                minorsecond="rgb(249, 229, 0)",
                majorsecond="rgb(249, 165, 0)",
                minorthird="rgb(0, 94, 0)",
                majorthird="rgb(0, 108, 0)",
                perfectfourth="rgb(0, 154, 0)",
                diminishedfifth="rgb(0, 15, 65)",
                perfectfifth="rgb(0, 73, 151)",
                minorsixth="rgb(168, 107, 98)",
                majorsixth="rgb(222, 81, 108)",
                minorseventh="rgb(120, 37, 134)",
                majorseventh="rgb(120, 25, 98)",
            ),
            fretted_colors=dict(
                root="rgb(231, 0, 0)",
                minorsecond="rgb(249, 229, 0)",
                majorsecond="rgb(249, 165, 0)",
                minorthird="rgb(0, 94, 0)",
                majorthird="rgb(0, 108, 0)",
                perfectfourth="rgb(0, 154, 0)",
                diminishedfifth="rgb(0, 15, 65)",
                perfectfifth="rgb(0, 73, 151)",
                minorsixth="rgb(168, 107, 98)",
                majorsixth="rgb(222, 81, 108)",
                minorseventh="rgb(120, 37, 134)",
                majorseventh="rgb(120, 25, 98)",
            ),
            enharmonic=True,
        ),
        background=dict(color="rgb(150,150,150)", opacity=0.2),
        fretnumber=dict(color="rgb(150,150,150)", fontsize=20, fontweight="bold"),
        neckdot=dict(
            color="rgb(200,200,200)",
            color_stroke="rgb(0,0,0)",
            width_stroke=2,
            radius=7,
        ),
        fret=dict(color="rgb(150,150,150)", width=3),
        nut=dict(color="rgb(0,0,0)", width=6),
        tuning=dict(
            color="rgb(150,150,150)",
            fontsize=20,
            fontweight="normal",
        ),
        string=dict(color="rgb(0,0,0)", width=3),
        open_note=dict(
            radius=20,
            color="rgb(255,255,255)",
            stroke_color="rgb(0,0,0)",
            stroke_width=3,
            text_color="rgb(0,0,0)",
            fontsize=20,
            fontweight="bold",
        ),
        fretted_note=dict(
            radius=20,
            color="rgb(255,255,255)",
            stroke_color="rgb(0,0,0)",
            stroke_width=3,
            text_color="rgb(0,0,0)",
            fontsize=20,
            fontweight="bold",
        ),
    )


@pytest.fixture()
def partial_dict_config():
    return dict(
        background=dict(color="blue"),
    )


def test_default_config(default_config: FretBoardConfig):
    assert default_config == FretBoardConfig()


def load_config_from_dict(dict_config):
    config = FretBoardConfig.from_dict(dict_config)
    assert config == FretBoardConfig()


def load_config_from_partial_dict(partial_dict_config):
    config = FretBoardConfig.from_dict(partial_dict_config)
    assert config.background.color == "blue"
    # The default is still there
    assert config.background.opacity == 0.2


def test_fretboard_get_background(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    background = fretboard.get_background()
    # Position == (width_fret + x_start, y_start)
    assert background.position == (100, 30)
    assert background.size == (840, 250)


def test_fretboard_get_background_new_tuning(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    fretboard.set_tuning(["E", "A", "D", "G"])
    background = fretboard.get_background()
    # Position == (width_fret + x_start, y_start)
    assert background.position == (100, 30)
    assert background.size == (840, 150)


def test_fretboard_get_neck_dots(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    neck_dots = fretboard.get_neck_dots()
    assert neck_dots[0].x == 275.0
    assert neck_dots[0].y == 155.0
    for neck_dot in neck_dots:
        # Check if center of fret
        assert (
            neck_dot.x
            % (fretboard.config.main.x_start - (fretboard.config.main.fret_width // 2))
            == 0
        )
        assert (
            neck_dot.y
            % (fretboard.config.main.y_start - (fretboard.config.main.fret_height // 2))
            == 0
        )


def test_fretboard_get_frets(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    frets = fretboard.get_frets()
    for fret in frets:
        # Test if multiple of width
        assert (
            fret.start_position[0] % fretboard.config.main.x_start
            + fretboard.config.main.fret_width
        )
        # Test if vertical line
        assert fret.start_position[0] == fret.end_position[0]

        # Test coherence and length
        assert fret.start_position[1] == fretboard.config.main.y_start
        assert fret.end_position[1] == (
            fretboard.config.main.y_start
            + (len(fretboard.tuning) - 1) * fretboard.config.main.fret_height
        )


def test_fretboard_get_strings(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    strings = fretboard.get_strings()
    for string in strings:
        # Test if horizontal line
        assert string.start_position[1] == string.end_position[1]

        # Test if multiple of width
        assert (
            string.start_position[1] % fretboard.config.main.x_start
            + fretboard.config.main.fret_height
        )

        # Test coherence and length
        assert (
            string.start_position[0]
            == fretboard.config.main.x_start + fretboard.config.main.fret_width
        )
        assert string.end_position[0] == (
            fretboard.config.main.y_start
            + fretboard.config.main.fret_width
            + fretboard.config.main.last_fret * fretboard.config.main.fret_width
        )


def test_fretboard_get_nut(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    nut = fretboard.get_nut()
    assert nut is not None
    # Test if vertical line
    assert nut.start_position[0] == nut.end_position[0]
    # Test if start where it should
    assert (
        nut.start_position[0]
        == fretboard.config.main.x_start + fretboard.config.main.fret_width
    )
    # Test if start where it should
    assert nut.start_position[1] == fretboard.config.main.y_start
    # Test length
    assert (
        nut.end_position[1]
        == fretboard.config.main.y_start
        + (len(fretboard.tuning) - 1) * fretboard.config.main.fret_height
    )


def test_fretboard_get_nut_not_first_fret(default_config: FretBoardConfig):
    default_config.main.first_fret = 1
    fretboard = FretBoard(config=default_config)
    nut = fretboard.get_nut()
    assert nut is None


def test_fretboard_get_fret_numbers(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    fret_numbers = fretboard.get_fret_numbers()
    assert fret_numbers is not None
    assert fret_numbers[0].x == 275.0
    assert fret_numbers[0].y == 330.0
    for fret_number in fret_numbers:
        # Check if center of fret
        assert (
            fret_number.x
            % (fretboard.config.main.x_start - (fretboard.config.main.fret_width // 2))
            == 0
        )
        assert (
            fret_number.y
            % (fretboard.config.main.y_start - (fretboard.config.main.fret_height // 2))
            == 0
        )


def test_fretboard_get_string(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    strings = fretboard.get_strings()
    for string in strings:
        # Test if horizontal line
        assert string.start_position[1] == string.end_position[1]

        # Test if multiple of width
        assert (
            string.start_position[1] % fretboard.config.main.x_start
            + fretboard.config.main.fret_height
        )

        # Test coherence and length
        assert (
            string.start_position[0]
            == fretboard.config.main.x_start + fretboard.config.main.fret_width
        )
        assert string.end_position[0] == (
            fretboard.config.main.y_start
            + fretboard.config.main.fret_width
            + fretboard.config.main.last_fret * fretboard.config.main.fret_width
        )


def test_fretboard_get_open_note(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    open_note = fretboard._get_open_note(position=(100, 100), note="C")
    assert open_note.x == 100
    assert open_note.y == 100
    assert open_note.name == "C"
    assert open_note.config.color == "rgb(255,255,255)"


def test_fretboard_get_open_note_root(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    open_note = fretboard._get_open_note(position=(100, 100), note="C", root="C")
    assert open_note.x == 100
    assert open_note.y == 100
    assert open_note.name == "C"
    assert open_note.config.color == "rgb(255,255,255)"


def test_fretboard_get_open_note_root_colors(default_config: FretBoardConfig):
    default_config.main.open_color_scale = True
    fretboard = FretBoard(config=default_config)
    open_note = fretboard._get_open_note(position=(100, 100), note="C", root="C")
    assert open_note.x == 100
    assert open_note.y == 100
    assert open_note.name == "C"
    # RED
    assert open_note.config.color == "rgb(231, 0, 0)"


def test_fretboard_get_open_note_show_degree_name(default_config: FretBoardConfig):
    default_config.main.open_color_scale = True
    default_config.main.show_degree_name = True
    fretboard = FretBoard(config=default_config)
    open_note = fretboard._get_open_note(position=(100, 100), note="C", root="C")
    assert open_note.x == 100
    assert open_note.y == 100
    assert open_note.name == "1"
    # RED
    assert open_note.config.color == "rgb(231, 0, 0)"


def test_fretboard_get_open_note_no_name(default_config: FretBoardConfig):
    default_config.main.open_color_scale = True
    default_config.main.show_degree_name = False
    default_config.main.show_note_name = False
    fretboard = FretBoard(config=default_config)
    open_note = fretboard._get_open_note(position=(100, 100), note="C", root="C")
    assert open_note.x == 100
    assert open_note.y == 100
    assert open_note.name == ""
    # RED
    assert open_note.config.color == "rgb(231, 0, 0)"


def test_fretboard_get_fretted_note(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    open_note = fretboard._get_fretted_note(position=(100, 100), note="C")
    assert open_note.x == 100
    assert open_note.y == 100
    assert open_note.name == "C"
    assert open_note.config.color == "rgb(255,255,255)"


def test_fretboard_get_fretted_note_root_colors(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    open_note = fretboard._get_fretted_note(position=(100, 100), note="C", root="C")
    assert open_note.x == 100
    assert open_note.y == 100
    assert open_note.name == "C"
    # RED
    assert open_note.config.color == "rgb(231, 0, 0)"


def test_fretboard_get_fretted_note_root_no_color(default_config: FretBoardConfig):
    default_config.main.fretted_color_scale = False
    fretboard = FretBoard(config=default_config)
    open_note = fretboard._get_fretted_note(position=(100, 100), note="C", root="C")
    assert open_note.x == 100
    assert open_note.y == 100
    assert open_note.name == "C"
    assert open_note.config.color == "rgb(255,255,255)"


def test_fretboard_get_fretted_note_show_degree_name(default_config: FretBoardConfig):
    default_config.main.show_degree_name = True
    fretboard = FretBoard(config=default_config)
    open_note = fretboard._get_fretted_note(position=(100, 100), note="C", root="C")
    assert open_note.x == 100
    assert open_note.y == 100
    assert open_note.name == "1"
    # RED
    assert open_note.config.color == "rgb(231, 0, 0)"


def test_fretboard_get_fretted_note_no_name(default_config: FretBoardConfig):
    default_config.main.show_degree_name = False
    default_config.main.show_note_name = False
    fretboard = FretBoard(config=default_config)
    open_note = fretboard._get_fretted_note(position=(100, 100), note="C", root="C")
    assert open_note.x == 100
    assert open_note.y == 100
    assert open_note.name == ""
    # RED
    assert open_note.config.color == "rgb(231, 0, 0)"


def test_fretboard_get_notes(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    notes = fretboard.get_notes(string_no=0, note="E", root="C")
    for note in notes:
        assert note.y == fretboard.config.main.y_start
        # Check if placed between two frets
        assert (
            note.x
            % (fretboard.config.main.x_start - (fretboard.config.main.fret_width // 2))
            == 0
        )


def test_fretboard_get_notes_invalid_string(default_config: FretBoardConfig):
    fretboard = FretBoard(config=default_config)
    with pytest.raises(ValueError):
        fretboard.get_notes(string_no=7, note="E", root="C")


def test_fretboard_get_bounds_fretboard(default_config):
    fretboard = FretBoard(config=default_config)
    upper_left, lower_right = fretboard.get_bounds_fretboard()
    assert upper_left == (30.0, 30.0)
    assert lower_right == (940.0, 280.0)


def test_init_fretboard(default_config):
    fretboard = FretBoard(config=default_config)
    fretboard.init_fretboard()
    assert len(fretboard.drawing.elements) == 38
    assert any(
        [isinstance(obj, svgwrite.shapes.Rect) for obj in fretboard.drawing.elements]
    )
    assert any(
        [isinstance(obj, svgwrite.shapes.Circle) for obj in fretboard.drawing.elements]
    )
    assert any(
        [isinstance(obj, svgwrite.shapes.Line) for obj in fretboard.drawing.elements]
    )
    assert any(
        [isinstance(obj, svgwrite.text.Text) for obj in fretboard.drawing.elements]
    )


def test_init_fretboard_add_scales(default_config):
    fretboard = FretBoard(config=default_config)
    notes_container = NotesContainer(
        root="C", notes=["C", "D", "E", "F", "G", "A", "B"]
    )
    fretboard.init_fretboard()
    fretboard.add_scale(notes_container)
    assert len(fretboard.drawing.elements) == 86
    assert any(
        [isinstance(obj, svgwrite.shapes.Rect) for obj in fretboard.drawing.elements]
    )
    assert any(
        [isinstance(obj, svgwrite.shapes.Circle) for obj in fretboard.drawing.elements]
    )
    assert any(
        [isinstance(obj, svgwrite.shapes.Line) for obj in fretboard.drawing.elements]
    )
    assert any(
        [isinstance(obj, svgwrite.text.Text) for obj in fretboard.drawing.elements]
    )


def test_add_element(default_config):
    note = OpenNote("C", position=(0, 0))
    fretboard = FretBoard(config=default_config)
    fretboard.add_element(note)


def test_add_wrong_lement(default_config):
    fretboard = FretBoard(config=default_config)
    with pytest.raises(ValueError):
        fretboard.add_element(1)
