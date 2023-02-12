from typing import List, Union, Tuple, Dict
import copy
import svgwrite
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from fretboardgtr.constants import STANDARD_TUNING, DOTS_POSITIONS
from fretboardgtr.elements.background import Background, BackgroundConfig
from fretboardgtr.elements.fret_number import FretNumber, FretNumberConfig
from fretboardgtr.elements.neck_dots import NeckDot, NeckDotConfig
from fretboardgtr.elements.frets import Fret, FretConfig
from fretboardgtr.elements.notes import (
    OpenNote,
    FrettedNote,
    OpenNoteConfig,
    FrettedNoteConfig,
)
from fretboardgtr.note_colors import NoteColors
from fretboardgtr.elements.nut import Nut, NutConfig
from fretboardgtr.elements.tuning import Tuning, TuningConfig
from fretboardgtr.elements.strings import String, StringConfig
from fretboardgtr.utils import (
    scale_to_intervals,
    chromatic_position_from_root,
    note_to_interval_name,
)
from fretboardgtr.notes_creators import NotesContainer
from dataclasses import dataclass
from typing import Optional
from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.exporters import PNGExporter, PDFExporter
from fretboardgtr.base import ConfigIniter


def get_valid_dots(first_fret: int, last_fret: int):
    dots = []
    for dot in DOTS_POSITIONS:
        if dot >= first_fret and dot <= last_fret:
            dots.append(dot)
    return dots


@dataclass
class FretBoardMainConfig:
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
    fretnumber: FretNumberConfig = FretNumberConfig()
    neckdot: NeckDotConfig = NeckDotConfig()
    fret: FretConfig = FretConfig()
    nut: NutConfig = NutConfig()
    tuning: TuningConfig = TuningConfig()
    string: StringConfig = StringConfig()
    open_note: OpenNoteConfig = OpenNoteConfig()
    fretted_note: FrettedNoteConfig = FrettedNoteConfig()


class FretBoard:
    def __init__(
        self,
        tuning: Optional[List[str]] = None,
        config: Optional[FretBoardConfig] = None,
    ):
        self.config = config if config is not None else FretBoardConfig()
        self.tuning = tuning if tuning is not None else STANDARD_TUNING
        self.drawing = self.get_empty()
        self._open_fret_width = self.config.main.fret_width

    def get_empty(self):
        """
        Create empty box and the object self.drawing
        """
        number_of_frets = self.config.main.last_fret - self.config.main.first_fret
        return svgwrite.Drawing(
            size=(  # +2 == Last fret + tuning
                self.config.main.x_start + self.config.main.fret_width * (number_of_frets + 2),
                self.config.main.y_start + self.config.main.fret_height * (len(self.tuning) + 1),
            ),
            profile="full",
        )

    def set_tuning(self, tuning: List[str]):
        self.tuning = tuning

    def get_background(self) -> Background:
        number_of_frets = self.config.main.last_fret - self.config.main.first_fret
        x = self.config.main.x_start + self._open_fret_width
        y = self.config.main.y_start
        width = (number_of_frets) * (self.config.main.fret_width)
        height = (len(self.tuning) - 1) * self.config.main.fret_height
        background = Background((x, y), (width, height), config=self.config.background)
        return background

    def add_background(self):
        """
        Add background component to the svg
        """
        background = self.get_background()
        self.drawing.add(background.get_svg())

    def get_neck_dots(self) -> List[NeckDot]:
        dots_elements = []
        dots = get_valid_dots(self.config.main.first_fret, self.config.main.last_fret)
        for dot in dots:
            x = (
                self.config.main.x_start
                + (0.5 + dot - self.config.main.first_fret) * self.config.main.fret_width
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
                upper_dot = NeckDot(upper_position, config=self.config.neckdot)
                lower_dot = NeckDot(lower_position, config=self.config.neckdot)
                dots_elements.append(upper_dot)
                dots_elements.append(lower_dot)
            else:
                center_position = (
                    x,
                    y,
                )
                center_dot = NeckDot(center_position, config=self.config.neckdot)
                dots_elements.append(center_dot)
        return dots_elements

    def add_neck_dots(self):
        """
        Add dot up to 24 frets.
        Recalculate if the minimum fret isn't 0 or maximum fret isn't 12.
        """
        dots = self.get_neck_dots()
        for dot in dots:
            self.drawing.add(dot.get_svg())

    def get_frets(self) -> List[Fret]:
        frets = []
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

            fret = Fret((x, y_start), (x, y_end), config=self.config.fret)
            frets.append(fret)
        return frets

    def add_frets(self):
        frets = self.get_frets()
        for fret in frets:
            self.drawing.add(fret.get_svg())

    def get_strings(self) -> List[String]:
        strings = []
        # begin before if min fret !=0 because no open chords
        x_start = self.config.main.x_start + self._open_fret_width
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
            string = String(start, end, config=self.config.string)
            strings.append(string)
        return strings

    def add_strings(self):
        # begin before if min fret !=0 because no open chords
        strings = self.get_strings()
        for string in strings:
            self.drawing.add(string.get_svg())

    def get_nut(self) -> Optional[Nut]:
        if self.config.main.first_fret != 0 or not self.config.main.show_nut:
            return None

        start = (
            self.config.main.x_start + self._open_fret_width,
            self.config.main.y_start,
        )
        end = (
            self.config.main.x_start + self._open_fret_width,
            self.config.main.y_start + self.config.main.fret_height * (len(self.tuning) - 1),
        )
        nut = Nut(start, end, config=self.config.nut)
        return nut

    def add_nut(self):
        """
        Create nut if minimum fret == 0.

        """
        nut = self.get_nut()
        if nut is None:
            return
        self.drawing.add(nut.get_svg())

    def get_fret_numbers(self) -> Optional[List[FretNumber]]:
        if not self.config.main.show_frets:
            return None
        fret_numbers = []
        dots = get_valid_dots(self.config.main.first_fret, self.config.main.last_fret)
        for dot in dots:
            x = self.config.main.x_start + self.config.main.fret_width * (
                1 / 2 + dot - self.config.main.first_fret
            )
            y = self.config.main.y_start + self.config.main.fret_height * (len(self.tuning))
            fret_number = FretNumber(str(dot), (x, y), config=self.config.fretnumber)
            fret_numbers.append(fret_number)
        return fret_numbers

    def add_fret_numbers(self):
        """
        Show text under the frets for example 3ft.
        """
        fret_numbers = self.get_fret_numbers()
        if fret_numbers is None:
            return None
        for fret_number in fret_numbers:
            self.drawing.add(fret_number.get_svg())

    def get_tuning(self) -> Optional[List[Tuning]]:
        if not self.config.main.show_tuning:
            return None
        tunings = []
        reversed_tuning = list(reversed(self.tuning))
        for i, note in enumerate(reversed_tuning):
            x = self.config.main.x_start + (
                self.config.main.fret_width
                * (self.config.main.last_fret - self.config.main.first_fret + 3 / 2)
            )
            y = self.config.main.y_start + self.config.main.fret_height * (i)
            tuning_note = Tuning(note, (x, y), config=self.config.tuning)
            tunings.append(tuning_note)
        return tunings

    def add_tuning(self):
        """
        Show tuning at the end of the neck.
        """

        tunings = self.get_tuning()
        if tunings is None:
            return None
        for tuning in tunings:
            self.drawing.add(tuning.get_svg())

    def init_fretboard(self):
        self.add_background()
        self.add_fret_numbers()
        self.add_frets()
        self.add_neck_dots()
        self.add_nut()
        self.add_strings()
        self.add_tuning()

    def _get_open_note(
        self, position: Tuple[float, float], note: str, root: Optional[str] = None
    ) -> OpenNote:
        config = copy.copy(self.config.open_note)
        if root and self.config.main.open_color_scale:
            idx = chromatic_position_from_root(root, note)
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
        config = copy.copy(self.config.fretted_note)
        if root and self.config.main.fretted_color_scale:
            idx = chromatic_position_from_root(root, note)
            color = self.config.main.fretted_colors.from_interval(idx)
            config.color = color

        if root and self.config.main.show_degree_name:
            note = note_to_interval_name(note, root)

        if not (self.config.main.show_degree_name or self.config.main.show_note_name):
            note = ""

        _note = FrettedNote(note, position, config=config)
        return _note

    def get_notes(
        self, string_no: int, note: str, root: Optional[str] = None
    ) -> List[Union[OpenNote, FrettedNote]]:
        if string_no < 0 or string_no > len(self.tuning):
            raise ValueError(f"String number is invalid. Tuning is {self.tuning}")

        string_root = self.tuning[len(self.tuning) - 1 - string_no]
        _idx = chromatic_position_from_root(string_root, note)

        indices = []
        while _idx <= self.config.main.last_fret:
            indices.append(_idx)
            _idx += 12
        notes = []
        for idx in indices:
            x = self.config.main.x_start + (self.config.main.fret_width) * (idx + (1 / 2))
            y = self.config.main.y_start + self.config.main.fret_height * (string_no)
            position = (x, y)
            _note: Union[OpenNote, FrettedNote]
            if idx == 0:
                _note = self._get_open_note(position, note, root)
            else:
                _note = self._get_fretted_note(position, note, root)
            notes.append(_note)
        return notes

    def add_notes(self, string_no: int, note: str, root: Optional[str] = None):
        notes = self.get_notes(string_no, note, root)
        for _note in notes:
            self.drawing.add(_note.get_svg())

    def add_scale(self, scale: NotesContainer):
        for string_no, _ in enumerate(self.tuning):
            for note in scale.notes:
                self.add_notes(string_no, note, scale.root)

    def get_bounds_fretboard(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        number_of_frets = self.config.main.last_fret - self.config.main.first_fret
        upper_left_x = self.config.main.x_start
        upper_left_y = self.config.main.y_start
        lower_right_x = (
            self.config.main.x_start
            + self._open_fret_width
            + (number_of_frets) * (self.config.main.fret_width)
        )
        lower_right_y = (
            self.config.main.y_start + (len(self.tuning) - 1) * self.config.main.fret_height
        )
        return ((upper_left_x, upper_left_y), (lower_right_x, lower_right_y))

    def add_element(self, element: FretBoardElement):
        if not issubclass(type(element), FretBoardElement):
            raise ValueError("Element should be a 'FretBoardElement'")
        self.drawing.add(element.get_svg())
