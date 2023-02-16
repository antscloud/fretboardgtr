import pytest

from fretboardgtr.elements.background import Background, BackgroundConfig
from fretboardgtr.elements.fret_number import FretNumber, FretNumberConfig
from fretboardgtr.elements.frets import Fret, FretConfig
from fretboardgtr.elements.neck_dots import NeckDot, NeckDotConfig
from fretboardgtr.elements.notes import (
    FrettedNote,
    FrettedNoteConfig,
    OpenNote,
    OpenNoteConfig,
)
from fretboardgtr.elements.nut import Nut, NutConfig
from fretboardgtr.elements.strings import String, StringConfig
from fretboardgtr.elements.tuning import Tuning, TuningConfig
from fretboardgtr.fretboards.config import FretBoardConfig, FretBoardGeneralConfig
from fretboardgtr.fretboards.vertical import VerticalFretBoardContainer
from fretboardgtr.note_colors import NoteColors
from fretboardgtr.notes_creators import NotesContainer


@pytest.fixture()
def default_config():
    return FretBoardConfig(
        general=FretBoardGeneralConfig(
            x_start=30.0,
            y_start=30.0,
            fret_height=50,
            fret_width=50,
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
        background=BackgroundConfig(color="none", opacity=0.7),
        fret_numbers=FretNumberConfig(
            color="rgb(150,150,150)", fontsize=20, fontweight="bold"
        ),
        neck_dots=NeckDotConfig(
            color="rgb(200,200,200)",
            color_stroke="rgb(0,0,0)",
            width_stroke=2,
            radius=7,
        ),
        frets=FretConfig(color="rgb(150,150,150)", width=3),
        nut=NutConfig(color="rgb(0,0,0)", width=6),
        tuning=TuningConfig(
            color="rgb(150,150,150)",
            fontsize=20,
            fontweight="normal",
        ),
        strings=StringConfig(color="rgb(0,0,0)", width=3),
        open_notes=OpenNoteConfig(
            radius=20,
            color="rgb(255,255,255)",
            stroke_color="rgb(0,0,0)",
            stroke_width=3,
            text_color="rgb(0,0,0)",
            fontsize=20,
            fontweight="bold",
        ),
        fretted_notes=FrettedNoteConfig(
            radius=20,
            color="rgb(255,255,255)",
            stroke_color="rgb(0,0,0)",
            stroke_width=3,
            text_color="rgb(0,0,0)",
            fontsize=20,
            fontweight="bold",
        ),
    )


def test_default_config_container(default_config):
    vertical_fretboard = VerticalFretBoardContainer()
    assert vertical_fretboard.config == default_config


def load_config_from_dict(dict_config):
    config = FretBoardConfig.from_dict(dict_config)
    assert config == FretBoardConfig()


def test_fretboard_get_background(default_config: FretBoardConfig):
    fretboard = VerticalFretBoardContainer(config=default_config)
    fretboard.add_background()
    background = fretboard.elements.background
    # Position == (width_fret + x_start, y_start)
    assert background.position == (80, 30)[::-1]
    assert background.size == (600, 250)[::-1]


def test_fretboard_get_background_new_tuning(default_config: FretBoardConfig):
    fretboard = VerticalFretBoardContainer(
        config=default_config, tuning=["E", "A", "D", "G"]
    )
    fretboard.add_background()
    background = fretboard.elements.background
    assert background.position == (80, 30)[::-1]
    assert background.size == (600, 150)[::-1]


def test_fretboard_get_neck_dots(default_config: FretBoardConfig):
    fretboard = VerticalFretBoardContainer(config=default_config)
    fretboard.add_neck_dots()
    neck_dots = fretboard.elements.neck_dots
    assert neck_dots[0].x == 155.0
    assert neck_dots[0].y == 205.0
    for neck_dot in neck_dots:
        # Check if center of fret
        assert (
            neck_dot.x
            % (
                fretboard.config.general.x_start
                - (fretboard.config.general.fret_width // 2)
            )
            == 0
        )
        assert (
            neck_dot.y
            % (
                fretboard.config.general.y_start
                - (fretboard.config.general.fret_height // 2)
            )
            == 0
        )


def test_fretboard_get_frets(default_config: FretBoardConfig):
    fretboard = VerticalFretBoardContainer(config=default_config)
    fretboard.add_frets()
    frets = fretboard.elements.frets
    for fret in frets:
        # Test if multiple of width
        assert (
            fret.start_position[0] % fretboard.config.general.x_start
            + fretboard.config.general.fret_width
        )
        # Test if Horizontal line
        assert fret.start_position[1] == fret.end_position[1]

        # Test coherence and length
        assert fret.start_position[0] == fretboard.config.general.x_start
        assert fret.end_position[0] == (
            fretboard.config.general.x_start
            + (len(fretboard.tuning) - 1) * fretboard.config.general.fret_width
        )


def test_fretboard_get_strings(default_config: FretBoardConfig):
    fretboard = VerticalFretBoardContainer(config=default_config)
    fretboard.add_strings()
    strings = fretboard.elements.strings
    for string in strings:
        # Test if vertical line
        assert string.start_position[0] == string.end_position[0]

        # Test if multiple of width
        assert (
            string.start_position[1] % fretboard.config.general.x_start
            + fretboard.config.general.fret_height
        )

        # Test coherence and length
        assert (
            string.start_position[1]
            == fretboard.config.general.y_start + fretboard.config.general.fret_height
        )
        assert string.end_position[1] == (
            fretboard.config.general.y_start
            + fretboard.config.general.fret_height
            + fretboard.config.general.last_fret * fretboard.config.general.fret_width
        )


def test_fretboard_get_nut(default_config: FretBoardConfig):
    fretboard = VerticalFretBoardContainer(config=default_config)
    fretboard.add_nut()
    nut = fretboard.elements.nut
    assert nut is not None
    # Test if horizontal line
    assert nut.start_position[1] == nut.end_position[1]
    # Test if start where it should
    assert (
        nut.start_position[1]
        == fretboard.config.general.y_start + fretboard.config.general.fret_height
    )

    # Test if start where it should
    assert nut.start_position[0] == fretboard.config.general.x_start
    # # Test length
    # assert nut.end_position[0] == (
    #     fretboard.config.general.x_start
    #     + (len(fretboard.tuning) - 1) * fretboard.config.general.fret_width
    # )


def test_fretboard_get_nut_not_first_fret(default_config: FretBoardConfig):
    default_config.general.first_fret = 1
    fretboard = VerticalFretBoardContainer(config=default_config)
    fretboard.add_nut()

    assert fretboard.elements.nut is None


def test_fretboard_get_fret_numbers(default_config: FretBoardConfig):
    fretboard = VerticalFretBoardContainer(config=default_config)
    fretboard.add_fret_numbers()
    fret_numbers = fretboard.elements.fret_numbers
    assert fret_numbers is not None
    assert fret_numbers[0].x == 330.0
    assert fret_numbers[0].y == 205.0
    for fret_number in fret_numbers:
        # Check if center of fret
        assert (
            fret_number.x
            % (
                fretboard.config.general.x_start
                - (fretboard.config.general.fret_width // 2)
            )
            == 0
        )
        assert (
            fret_number.y
            % (
                fretboard.config.general.y_start
                - (fretboard.config.general.fret_height // 2)
            )
            == 0
        )


def test_fretboard_get_notes(default_config: FretBoardConfig):
    fretboard = VerticalFretBoardContainer(config=default_config)
    fretboard.add_note(string_no=0, note="E", root="C")

    notes = fretboard.elements.notes
    for note in notes:
        assert note.x == fretboard.config.general.x_start
        # Check if placed between two frets
        assert (
            note.y
            % (
                fretboard.config.general.y_start
                - (fretboard.config.general.fret_width // 2)
            )
            == 0
        )


def test_fretboard_get_notes_invalid_string(default_config: FretBoardConfig):
    fretboard = VerticalFretBoardContainer(config=default_config)
    with pytest.raises(ValueError):
        fretboard.add_note(string_no=7, note="E", root="C")


def test_fretboard_get_inside_bounds(default_config):
    fretboard = VerticalFretBoardContainer(config=default_config)
    upper_left, lower_right = fretboard.get_inside_bounds()
    assert upper_left == (30.0, 30.0)
    assert lower_right == (280.0, 680.0)


def test_fretboard_get_size(default_config):
    fretboard = VerticalFretBoardContainer(config=default_config)
    width, height = fretboard.get_size()
    assert width == 380.0
    assert height == 730.0


def test_init_fretboard(default_config):
    fretboard = VerticalFretBoardContainer(config=default_config)
    assert len(fretboard.elements) == 37
    assert len(fretboard.elements.strings) == 6
    assert len(fretboard.elements.frets) == 12
    list_of_elements = fretboard.elements.to_list()
    assert any([isinstance(obj, FretNumber) for obj in list_of_elements])
    assert any([isinstance(obj, Fret) for obj in list_of_elements])
    assert any([isinstance(obj, NeckDot) for obj in list_of_elements])
    assert any([isinstance(obj, Nut) for obj in list_of_elements])
    assert any([isinstance(obj, String) for obj in list_of_elements])
    assert any([isinstance(obj, Tuning) for obj in list_of_elements])
    assert not any([isinstance(obj, FrettedNote) for obj in list_of_elements])
    assert not any([isinstance(obj, OpenNote) for obj in list_of_elements])


def test_init_fretboard_add_scales(default_config):
    fretboard = VerticalFretBoardContainer(config=default_config)
    notes_container = NotesContainer(
        root="C", notes=["C", "D", "E", "F", "G", "A", "B"]
    )
    fretboard.add_scale(notes_container)
    assert len(fretboard.elements) == 85
    assert len(fretboard.elements.strings) == 6
    assert len(fretboard.elements.frets) == 12
    list_of_elements = fretboard.elements.to_list()
    assert any([isinstance(obj, Background) for obj in list_of_elements])
    assert any([isinstance(obj, FretNumber) for obj in list_of_elements])
    assert any([isinstance(obj, Fret) for obj in list_of_elements])
    assert any([isinstance(obj, NeckDot) for obj in list_of_elements])
    assert any([isinstance(obj, Nut) for obj in list_of_elements])
    assert any([isinstance(obj, String) for obj in list_of_elements])
    assert any([isinstance(obj, Tuning) for obj in list_of_elements])
    assert any([isinstance(obj, FrettedNote) for obj in list_of_elements])
    assert any([isinstance(obj, OpenNote) for obj in list_of_elements])


def test_add_element(default_config):
    note = OpenNote("C", position=(0, 0))
    fretboard = VerticalFretBoardContainer(config=default_config)
    fretboard.add_element(note)


def test_add_wrong_lement(default_config):
    fretboard = VerticalFretBoardContainer(config=default_config)
    with pytest.raises(ValueError):
        fretboard.add_element(1)
