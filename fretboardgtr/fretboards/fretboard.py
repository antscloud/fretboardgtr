import copy
import os
import sys
from typing import List, Tuple, Union

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from typing import Optional

from fretboardgtr.constants import STANDARD_TUNING
from fretboardgtr.elements.background import Background
from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.elements.cross import Cross
from fretboardgtr.elements.fret_number import FretNumber
from fretboardgtr.elements.frets import Fret
from fretboardgtr.elements.neck_dots import NeckDot
from fretboardgtr.elements.notes import FrettedNote, OpenNote
from fretboardgtr.elements.nut import Nut
from fretboardgtr.elements.strings import String
from fretboardgtr.elements.tuning import Tuning
from fretboardgtr.fretboards.base import FretBoardLike
from fretboardgtr.fretboards.config import FretBoardConfig
from fretboardgtr.fretboards.elements import FretBoardElements
from fretboardgtr.notes_creators import NotesContainer
from fretboardgtr.utils import (
    chromatic_position_from_root,
    get_note_from_index,
    get_valid_dots,
    note_to_interval_name,
)


class FretBoardContainer(FretBoardLike):
    def __init__(
        self,
        tuning: Optional[List[str]] = None,
        config: Optional[FretBoardConfig] = None,
    ):
        self.config = config if config is not None else FretBoardConfig()
        self.tuning = tuning if tuning is not None else STANDARD_TUNING
        self.elements = FretBoardElements()
        self.init()

    def set_config(self, config: FretBoardConfig) -> None:
        self.config = config

    def init(self) -> None:
        self.add_background()
        self.add_fret_numbers()
        self.add_neck_dots()
        self.add_frets()
        self.add_nut()
        self.add_tuning()
        self.add_strings()

    def add_background(self) -> None:
        number_of_frets = self.config.general.last_fret - self.config.general.first_fret
        open_fret_width = self.config.general.fret_width
        x = self.config.general.x_start + open_fret_width
        y = self.config.general.y_start
        width = (number_of_frets) * (self.config.general.fret_width)
        height = (len(self.tuning) - 1) * self.config.general.fret_height
        background = Background((x, y), (width, height), config=self.config.background)
        self.elements.background = background

    def add_neck_dots(self) -> None:
        dots = get_valid_dots(
            self.config.general.first_fret, self.config.general.last_fret
        )
        for dot in dots:
            x = (
                self.config.general.x_start
                + (0.5 + dot - self.config.general.first_fret)
                * self.config.general.fret_width
            )
            y = (
                self.config.general.y_start
                + (len(self.tuning) / 2 - (1 / 2)) * self.config.general.fret_height
            )
            if dot % 12 == 0:
                # Add two dots dot is multiple of 12
                lower_position = (
                    x,
                    y - self.config.general.fret_height,
                )
                upper_position = (
                    x,
                    y + self.config.general.fret_height,
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
        show_nut = self.config.general.show_nut
        number_of_frets = self.config.general.last_fret - self.config.general.first_fret

        # Skip the open virtual fret
        first_fret = 1
        if self.config.general.first_fret == 0 and show_nut:
            first_fret = 2

        # +2 is to close the last fret of fretboard
        for fret_no in range(first_fret, number_of_frets + 2):
            x = self.config.general.x_start + (self.config.general.fret_width) * (
                fret_no
            )
            y_start = self.config.general.y_start
            y_end = self.config.general.y_start + (self.config.general.fret_height) * (
                len(self.tuning) - 1
            )

            fret = Fret((x, y_start), (x, y_end), config=self.config.frets)
            self.elements.frets.append(fret)

    def add_strings(self) -> None:
        # begin before if min fret !=0 because no open chords
        open_fret_width = self.config.general.fret_width
        x_start = self.config.general.x_start + open_fret_width
        x_end = self.config.general.x_start + (
            self.config.general.fret_width
            + (self.config.general.last_fret - self.config.general.first_fret)
            * self.config.general.fret_width
        )

        for i, _ in enumerate(self.tuning):
            start = (
                x_start,
                self.config.general.y_start + (self.config.general.fret_height) * (i),
            )
            end = (
                x_end,
                self.config.general.y_start + (self.config.general.fret_height) * (i),
            )
            string = String(start, end, config=self.config.strings)
            self.elements.strings.append(string)

    def add_nut(self) -> None:
        if self.config.general.first_fret != 0 or not self.config.general.show_nut:
            return None
        open_fret_width = self.config.general.fret_width

        start = (
            self.config.general.x_start + open_fret_width,
            self.config.general.y_start,
        )
        end = (
            self.config.general.x_start + open_fret_width,
            self.config.general.y_start
            + self.config.general.fret_height * (len(self.tuning) - 1),
        )
        nut = Nut(start, end, config=self.config.nut)
        self.elements.nut = nut

    def add_fret_numbers(self) -> None:
        if not self.config.general.show_frets:
            return None

        dots = get_valid_dots(
            self.config.general.first_fret, self.config.general.last_fret
        )
        for dot in dots:
            x = self.config.general.x_start + self.config.general.fret_width * (
                1 / 2 + dot - self.config.general.first_fret
            )
            y = self.config.general.y_start + self.config.general.fret_height * (
                len(self.tuning)
            )
            fret_number = FretNumber(str(dot), (x, y), config=self.config.fret_numbers)
            self.elements.fret_numbers.append(fret_number)

    def add_tuning(self) -> None:
        if not self.config.general.show_tuning:
            return None
        reversed_tuning = list(reversed(self.tuning))
        for i, note in enumerate(reversed_tuning):
            x = self.config.general.x_start + (
                self.config.general.fret_width
                * (
                    self.config.general.last_fret
                    - self.config.general.first_fret
                    + 3 / 2
                )
            )
            y = self.config.general.y_start + self.config.general.fret_height * (i)
            tuning_note = Tuning(note, (x, y), config=self.config.tuning)
            self.elements.tuning.append(tuning_note)

    def _get_open_note(
        self, position: Tuple[float, float], note: str, root: Optional[str] = None
    ) -> OpenNote:
        config = copy.copy(self.config.open_notes)
        if root and self.config.general.open_color_scale:
            idx = chromatic_position_from_root(note, root)
            color = self.config.general.open_colors.from_interval(idx)
            config.color = color

        if root and self.config.general.show_degree_name:
            note = note_to_interval_name(note, root)

        if not (
            self.config.general.show_degree_name or self.config.general.show_note_name
        ):
            note = ""

        _note = OpenNote(note, position, config=config)
        return _note

    def _get_fretted_note(
        self, position: Tuple[float, float], note: str, root: Optional[str] = None
    ) -> FrettedNote:
        config = copy.copy(self.config.fretted_notes)
        if root and self.config.general.fretted_color_scale:
            idx = chromatic_position_from_root(note, root)
            color = self.config.general.fretted_colors.from_interval(idx)
            config.color = color

        if root and self.config.general.show_degree_name:
            note = note_to_interval_name(note, root)

        if not (
            self.config.general.show_degree_name or self.config.general.show_note_name
        ):
            note = ""

        _note = FrettedNote(note, position, config=config)
        return _note

    def add_note(self, string_no: int, note: str, root: Optional[str] = None) -> None:
        if string_no < 0 or string_no > len(self.tuning):
            raise ValueError(f"String number is invalid. Tuning is {self.tuning}")

        string_root = self.tuning[len(self.tuning) - 1 - string_no]
        _idx = chromatic_position_from_root(note, string_root)

        indices = []
        while _idx <= self.config.general.last_fret:
            indices.append(_idx)
            _idx += 12

        for idx in indices:
            x = self.config.general.x_start + (self.config.general.fret_width) * (
                idx + (1 / 2)
            )
            y = self.config.general.y_start + self.config.general.fret_height * (
                string_no
            )
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

    def add_fingering(
        self, fingering: List[Optional[int]], root: Optional[str] = None
    ) -> None:
        """Add fingerinf starting with upper string to lower string."""
        if len(fingering) != len(self.tuning):
            raise ValueError(
                f"Fingering has not the same size as tuning."
                f" Got {len(fingering)} expected {len(self.tuning)}"
            )

        for string_no, finger_position in enumerate(reversed(fingering)):
            string_note = self.tuning[len(self.tuning) - 1 - string_no]
            if finger_position is None:
                x = self.config.general.x_start + self.config.general.fret_width * (
                    1 / 2
                )
                y = self.config.general.y_start + (self.config.general.fret_height) * (
                    string_no
                )
                position = (x, y)
                cross = Cross(position, config=self.config.cross)
                self.elements.crosses.append(cross)
            else:
                x = self.config.general.x_start + self.config.general.fret_width * (
                    1 / 2 + finger_position
                )
                y = self.config.general.y_start + (self.config.general.fret_height) * (
                    string_no
                )

                position = (x, y)
                note_name = get_note_from_index(finger_position, string_note)

                _note: Union[OpenNote, FrettedNote]
                if finger_position == 0:
                    _note = self._get_open_note(position, note_name, root)
                else:
                    _note = self._get_fretted_note(position, note_name, root)

                self.elements.notes.append(_note)

    def get_size(self) -> Tuple[float, float]:
        number_of_frets = self.config.general.last_fret - self.config.general.first_fret
        width = (
            self.config.general.x_start
            + self.config.general.fret_width * (number_of_frets + 2)
            + self.config.general.x_end_offset
        )
        height = (
            self.config.general.y_start
            + self.config.general.fret_height * (len(self.tuning) + 1)
            + self.config.general.y_end_offset
        )
        return (width, height)

    def get_inside_bounds(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        open_fret_width = self.config.general.fret_width
        number_of_frets = self.config.general.last_fret - self.config.general.first_fret
        upper_left_x = self.config.general.x_start
        upper_left_y = self.config.general.y_start
        lower_right_x = (
            self.config.general.x_start
            + open_fret_width
            + (number_of_frets) * (self.config.general.fret_width)
        )
        lower_right_y = (
            self.config.general.y_start
            + (len(self.tuning) - 1) * self.config.general.fret_height
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

    def get_elements(self) -> FretBoardElements:
        return self.elements
