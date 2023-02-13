import copy
import os
import sys
from pathlib import Path
from typing import List, Literal, Tuple, Union

import svgwrite

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from dataclasses import dataclass, field, fields
from typing import Optional

from fretboardgtr.base import ConfigIniter
from fretboardgtr.constants import DOTS_POSITIONS, STANDARD_TUNING
from fretboardgtr.elements.background import Background, BackgroundConfig
from fretboardgtr.elements.base import FretBoardElement
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
from fretboardgtr.exporters import EXPORTERS
from fretboardgtr.note_colors import NoteColors
from fretboardgtr.notes_creators import NotesContainer
from fretboardgtr.utils import chromatic_position_from_root, note_to_interval_name


def get_valid_dots(first_fret: int, last_fret: int):
    dots = []
    for dot in DOTS_POSITIONS:
        if dot >= first_fret and dot <= last_fret:
            dots.append(dot)
    return dots


@dataclass
class FretBoardMainConfig(ConfigIniter):
    x_start: float = 30.0
    y_start: float = 30.0
    fret_height: int = 50
    fret_width: int = 70
    first_fret: int = 0
    last_fret: int = 12
    show_tuning: bool = True
    show_frets: bool = True
    show_nut: bool = True
    show_degree_name: bool = False
    show_note_name: bool = True
    open_color_scale: bool = False
    fretted_color_scale: bool = True
    open_colors: NoteColors = NoteColors()
    fretted_colors: NoteColors = NoteColors()
    enharmonic: bool = True


@dataclass
class FretBoardConfig(ConfigIniter):
    main: FretBoardMainConfig = FretBoardMainConfig()
    background: BackgroundConfig = BackgroundConfig()
    fret_numbers: FretNumberConfig = FretNumberConfig()
    neck_dots: NeckDotConfig = NeckDotConfig()
    frets: FretConfig = FretConfig()
    nut: NutConfig = NutConfig()
    tuning: TuningConfig = TuningConfig()
    strings: StringConfig = StringConfig()
    open_notes: OpenNoteConfig = OpenNoteConfig()
    fretted_notes: FrettedNoteConfig = FrettedNoteConfig()


@dataclass
class FretBoardElements:
    background: Optional[Background] = None
    fret_numbers: List[FretNumber] = field(default_factory=list)
    neck_dots: List[NeckDot] = field(default_factory=list)
    frets: List[Fret] = field(default_factory=list)
    nut: Optional[Nut] = None
    tuning: List[Tuning] = field(default_factory=list)
    strings: List[String] = field(default_factory=list)
    notes: List[Union[OpenNote, FrettedNote]] = field(default_factory=list)
    customs: List[FretBoardElement] = field(default_factory=list)

    def to_list(self) -> List[FretBoardElement]:
        flat_elements = []
        for element in fields(self):
            value = getattr(self, element.name)
            if isinstance(value, list):
                flat_elements.extend(value)
            elif value is not None:
                flat_elements.append(value)
        return flat_elements

    def __len__(self) -> int:
        return len(self.to_list())


class FretBoardContainer:
    def __init__(
        self,
        tuning: Optional[List[str]] = None,
        config: Optional[FretBoardConfig] = None,
    ):
        self.config = config if config is not None else FretBoardConfig()
        self.tuning = tuning if tuning is not None else STANDARD_TUNING
        self.elements = FretBoardElements()
        self.init()

    def init(self):
        self.add_background()
        self.add_fret_numbers()
        self.add_neck_dots()
        self.add_frets()
        self.add_nut()
        self.add_tuning()
        self.add_strings()

    def add_background(self) -> None:
        number_of_frets = self.config.main.last_fret - self.config.main.first_fret
        open_fret_width = self.config.main.fret_width
        x = self.config.main.x_start + open_fret_width
        y = self.config.main.y_start
        width = (number_of_frets) * (self.config.main.fret_width)
        height = (len(self.tuning) - 1) * self.config.main.fret_height
        background = Background((x, y), (width, height), config=self.config.background)
        self.elements.background = background

    def add_neck_dots(self) -> None:
        dots = get_valid_dots(self.config.main.first_fret, self.config.main.last_fret)
        for dot in dots:
            x = (
                self.config.main.x_start
                + (0.5 + dot - self.config.main.first_fret)
                * self.config.main.fret_width
            )
            y = (
                self.config.main.y_start
                + (len(self.tuning) / 2 - (1 / 2)) * self.config.main.fret_height
            )
            if dot % 12 == 0:
                # Add two dots dot is multiple of 12
                lower_position = (
                    x,
                    y - self.config.main.fret_height,
                )
                upper_position = (
                    x,
                    y + self.config.main.fret_height,
                )
                upper_dot = NeckDot(upper_position, config=self.config.neck_dots)
                lower_dot = NeckDot(lower_position, config=self.config.neck_dots)
                self.elements.neck_dots.append(upper_dot)
                self.elements.neck_dots.append(lower_dot)
            else:
                center_position = (
                    x,
                    y,
                )
                center_dot = NeckDot(center_position, config=self.config.neck_dots)
                self.elements.neck_dots.append(center_dot)

    def add_frets(self) -> None:
        show_nut = self.config.main.show_nut
        number_of_frets = self.config.main.last_fret - self.config.main.first_fret

        # Skip the open virtual fret
        first_fret = 1
        if self.config.main.first_fret == 0 and show_nut:
            first_fret = 2

        # +2 is to close the last fret of fretboard
        for fret_no in range(first_fret, number_of_frets + 2):
            x = self.config.main.x_start + (self.config.main.fret_width) * (fret_no)
            y_start = self.config.main.y_start
            y_end = self.config.main.y_start + (self.config.main.fret_height) * (
                len(self.tuning) - 1
            )

            fret = Fret((x, y_start), (x, y_end), config=self.config.frets)
            self.elements.frets.append(fret)

    def add_strings(self) -> None:
        # begin before if min fret !=0 because no open chords
        open_fret_width = self.config.main.fret_width
        x_start = self.config.main.x_start + open_fret_width
        x_end = self.config.main.x_start + (
            self.config.main.fret_width
            + (self.config.main.last_fret - self.config.main.first_fret)
            * self.config.main.fret_width
        )

        for i, _ in enumerate(self.tuning):
            start = (
                x_start,
                self.config.main.y_start + (self.config.main.fret_height) * (i),
            )
            end = (
                x_end,
                self.config.main.y_start + (self.config.main.fret_height) * (i),
            )
            string = String(start, end, config=self.config.strings)
            self.elements.strings.append(string)

    def add_nut(self) -> None:
        if self.config.main.first_fret != 0 or not self.config.main.show_nut:
            return None
        open_fret_width = self.config.main.fret_width

        start = (
            self.config.main.x_start + open_fret_width,
            self.config.main.y_start,
        )
        end = (
            self.config.main.x_start + open_fret_width,
            self.config.main.y_start
            + self.config.main.fret_height * (len(self.tuning) - 1),
        )
        nut = Nut(start, end, config=self.config.nut)
        self.elements.nut = nut

    def add_fret_numbers(self) -> None:
        if not self.config.main.show_frets:
            return None

        dots = get_valid_dots(self.config.main.first_fret, self.config.main.last_fret)
        for dot in dots:
            x = self.config.main.x_start + self.config.main.fret_width * (
                1 / 2 + dot - self.config.main.first_fret
            )
            y = self.config.main.y_start + self.config.main.fret_height * (
                len(self.tuning)
            )
            fret_number = FretNumber(str(dot), (x, y), config=self.config.fret_numbers)
            self.elements.fret_numbers.append(fret_number)

    def add_tuning(self) -> None:
        if not self.config.main.show_tuning:
            return None
        reversed_tuning = list(reversed(self.tuning))
        for i, note in enumerate(reversed_tuning):
            x = self.config.main.x_start + (
                self.config.main.fret_width
                * (self.config.main.last_fret - self.config.main.first_fret + 3 / 2)
            )
            y = self.config.main.y_start + self.config.main.fret_height * (i)
            tuning_note = Tuning(note, (x, y), config=self.config.tuning)
            self.elements.tuning.append(tuning_note)

    def _get_open_note(
        self, position: Tuple[float, float], note: str, root: Optional[str] = None
    ) -> OpenNote:
        config = copy.copy(self.config.open_notes)
        if root and self.config.main.open_color_scale:
            idx = chromatic_position_from_root(note, root)
            color = self.config.main.open_colors.from_interval(idx)
            config.color = color

        if root and self.config.main.show_degree_name:
            note = note_to_interval_name(note, root)

        if not (self.config.main.show_degree_name or self.config.main.show_note_name):
            note = ""

        _note = OpenNote(note, position, config=config)
        return _note

    def _get_fretted_note(
        self, position: Tuple[float, float], note: str, root: Optional[str] = None
    ) -> FrettedNote:
        config = copy.copy(self.config.fretted_notes)
        if root and self.config.main.fretted_color_scale:
            idx = chromatic_position_from_root(note, root)
            color = self.config.main.fretted_colors.from_interval(idx)
            config.color = color

        if root and self.config.main.show_degree_name:
            note = note_to_interval_name(note, root)

        if not (self.config.main.show_degree_name or self.config.main.show_note_name):
            note = ""

        _note = FrettedNote(note, position, config=config)
        return _note

    def add_note(self, string_no: int, note: str, root: Optional[str] = None) -> None:
        if string_no < 0 or string_no > len(self.tuning):
            raise ValueError(f"String number is invalid. Tuning is {self.tuning}")

        string_root = self.tuning[len(self.tuning) - 1 - string_no]
        _idx = chromatic_position_from_root(note, string_root)

        indices = []
        while _idx <= self.config.main.last_fret:
            indices.append(_idx)
            _idx += 12

        for idx in indices:
            x = self.config.main.x_start + (self.config.main.fret_width) * (
                idx + (1 / 2)
            )
            y = self.config.main.y_start + self.config.main.fret_height * (string_no)
            position = (x, y)
            _note: Union[OpenNote, FrettedNote]
            if idx == 0:
                _note = self._get_open_note(position, note, root)
            else:
                _note = self._get_fretted_note(position, note, root)
            self.elements.notes.append(_note)

    def add_scale(self, scale: NotesContainer) -> None:
        for string_no, _ in enumerate(self.tuning):
            for note in scale.notes:
                self.add_note(string_no, note, scale.root)

    def get_bounds_of_fretboard(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        open_fret_width = self.config.main.fret_width
        number_of_frets = self.config.main.last_fret - self.config.main.first_fret
        upper_left_x = self.config.main.x_start
        upper_left_y = self.config.main.y_start
        lower_right_x = (
            self.config.main.x_start
            + open_fret_width
            + (number_of_frets) * (self.config.main.fret_width)
        )
        lower_right_y = (
            self.config.main.y_start
            + (len(self.tuning) - 1) * self.config.main.fret_height
        )
        return ((upper_left_x, upper_left_y), (lower_right_x, lower_right_y))

    def add_note_element(self, note: Union[OpenNote, FrettedNote]) -> None:
        if not issubclass(type(note), OpenNote) or issubclass(type(note), FrettedNote):
            raise ValueError("Element should be either 'OpenNote' or 'FrettedNoted'")
        self.elements.notes.append(note)

    def add_element(self, element: FretBoardElement) -> None:
        if not issubclass(type(element), FretBoardElement):
            raise ValueError("Element should be a 'FretBoardElement'")
        self.elements.customs.append(element)


class FretboardDrawer:
    def __init__(self, fretboard: FretBoardContainer):
        self._fretboard = fretboard
        self.drawing = self.get_empty()

    def get_empty(self) -> svgwrite.Drawing:
        """Create empty box and the object self.drawing."""
        number_of_frets = (
            self._fretboard.config.main.last_fret
            - self._fretboard.config.main.first_fret
        )
        return svgwrite.Drawing(
            size=(  # +2 == Last fret + tuning
                self._fretboard.config.main.x_start
                + self._fretboard.config.main.fret_width * (number_of_frets + 2),
                self._fretboard.config.main.y_start
                + self._fretboard.config.main.fret_height
                * (len(self._fretboard.tuning) + 1),
            ),
            profile="full",
        )

    def add_to_drawing(self, element: FretBoardElement):
        if not issubclass(type(element), FretBoardElement):
            raise ValueError(f"Element {element} does not subclass FretBoardElement")
        self.drawing.add(element.get_svg())

    def draw(self):
        for key in fields(self._fretboard.elements):
            element = getattr(self._fretboard.elements, key.name)
            if isinstance(element, list):
                for sub in element:
                    self.add_to_drawing(sub)
            else:
                self.add_to_drawing(element)


class FretBoard:
    def __init__(
        self,
        tuning: Optional[List[str]] = None,
        config: Optional[FretBoardConfig] = None,
    ):
        self._fretboard = FretBoardContainer(config=config, tuning=tuning)

    def set_config(self, config: FretBoardConfig) -> None:
        if not issubclass(type(config), FretBoardConfig):
            raise ValueError(f"scale should be a FretBoardConfig nor {type(config)}")
        self.config = config
        self._fretboard.config = config

    def add_notes(self, scale: NotesContainer) -> None:
        if not issubclass(type(scale), NotesContainer):
            raise ValueError(f"scale should be a NotesContainer nor {type(scale)}")
        self._fretboard.add_scale(scale=scale)

    def add_note_element(self, note: Union[OpenNote, FrettedNote]) -> None:
        self._fretboard.add_note_element(note)

    def add_element(self, element: FretBoardElement) -> None:
        self._fretboard.add_element(element)

    def get_bounds_of_fretboard(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        return self._fretboard.get_bounds_of_fretboard()

    def export(
        self, to: Union[Path, str], format: Literal["svg", "png", "pdf"] = "svg"
    ) -> None:
        if format.upper() not in EXPORTERS:
            availables = ", ".join(list(EXPORTERS.keys()))
            raise NotImplementedError(
                f"Save to the {format} format is unsupported."
                f" Available formats are {availables}"
            )
        drawer = FretboardDrawer(self._fretboard)
        drawer.draw()
        EXPORTERS[format.upper()](drawer.drawing).export(to=to)
