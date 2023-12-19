import copy
from pathlib import Path
from typing import Dict, List, Literal, Optional, Tuple, Union

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
from fretboardgtr.exporters import EXPORTERS
from fretboardgtr.fretboards.base import FretBoardLike
from fretboardgtr.fretboards.config import FretBoardConfig
from fretboardgtr.fretboards.converters import FretBoardToSVGConverter
from fretboardgtr.fretboards.elements import FretBoardElements
from fretboardgtr.fretboards.horizontal import HorizontalFretBoard
from fretboardgtr.fretboards.vertical import VerticalFretBoard
from fretboardgtr.notes_creators import NotesContainer
from fretboardgtr.utils import (
    chromatic_position_from_root,
    get_note_from_index,
    get_valid_dots,
    note_to_interval_name,
    scale_to_enharmonic,
)


def build_config(config: Optional[Union[Dict, FretBoardConfig]]) -> FretBoardConfig:
    if config is None:
        return FretBoardConfig()
    elif isinstance(config, dict):
        return FretBoardConfig.from_dict(config)
    elif isinstance(config, FretBoardConfig):
        return config
    else:
        msg = "Invalid config type {type(config)}."
        msg += "Need a dictionnary or FretBoardConfig instance"
        raise ValueError(msg)


class FretBoard(FretBoardLike):
    def __init__(
        self,
        tuning: Optional[List[str]] = None,
        config: Optional[Union[Dict, FretBoardConfig]] = None,
        vertical: bool = False,
    ):
        self.tuning = tuning if tuning is not None else STANDARD_TUNING

        self.config = build_config(config)
        self.elements = FretBoardElements()
        self.fretboard: Union[HorizontalFretBoard, VerticalFretBoard] = (
            HorizontalFretBoard(tuning, self.config)
            if not vertical
            else VerticalFretBoard(tuning, self.config)
        )
        self.init()

    def set_config(self, config: FretBoardConfig) -> None:
        self.config = config

    def init(self) -> None:
        """Init the fretboard by adding essential elements.

        This adds :
            background
            fret_numbers
            neck_dots
            frets
            nut
            tuning
            strings
        """
        self.add_background()
        self.add_fret_numbers()
        self.add_neck_dots()
        self.add_frets()
        self.add_nut()
        self.add_tuning()
        self.add_strings()

    def add_background(self) -> None:
        """Build and add background element."""
        x, y = self.fretboard.get_background_start_position()
        width, height = self.fretboard.get_background_dimensions()
        background = Background((x, y), (width, height), config=self.config.background)
        self.elements.background = background

    def add_neck_dots(self) -> None:
        """Build and add neck dot elements."""
        dots = get_valid_dots(
            self.config.general.first_fret, self.config.general.last_fret
        )
        for dot in dots:
            for position in self.fretboard.get_neck_dot_position(dot):
                center_dot = NeckDot(position, config=self.config.neck_dots)
                self.elements.neck_dots.append(center_dot)

    def add_frets(self) -> None:
        """Build and add fret elements."""
        show_nut = self.config.general.show_nut
        number_of_frets = self.config.general.last_fret - self.config.general.first_fret

        # Skip the open virtual fret
        first_fret = 0
        if show_nut:
            first_fret = 1

        # +2 is to close the last fret of fretboard
        for fret_no in range(first_fret, number_of_frets + 2):
            position = self.fretboard.get_fret_position(fret_no)

            fret = Fret(position[0], position[1], config=self.config.frets)
            self.elements.frets.append(fret)

    def add_strings(self) -> None:
        """Build and add string elements."""
        # begin before if min fret !=0 because no open chords

        for string_no, _ in enumerate(self.tuning):
            start, end = self.fretboard.get_strings_position(string_no)
            string = String(start, end, config=self.config.strings)
            self.elements.strings.append(string)

    def add_nut(self) -> None:
        """Build and add nut element."""
        position = self.fretboard.get_nut_position()
        if not position:
            return None
        start, end = position
        nut = Nut(start, end, config=self.config.nut)
        self.elements.nut = nut

    def add_fret_numbers(self) -> None:
        """Build and add fret number elements."""
        if not self.config.general.show_frets:
            return None

        dots = get_valid_dots(
            self.config.general.first_fret, self.config.general.last_fret
        )
        for dot in dots:
            x, y = self.fretboard.get_fret_number_position(dot)
            fret_number = FretNumber(str(dot), (x, y), config=self.config.fret_numbers)
            self.elements.fret_numbers.append(fret_number)

    def add_tuning(self) -> None:
        """Build and add tuning element."""
        if not self.config.general.show_tuning:
            return None
        tuning = self.fretboard.get_list_in_good_order(self.tuning)
        for string_no, note in enumerate(tuning):
            x, y = self.fretboard.get_tuning_position(string_no)
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

    def _add_single_note(
        self, string_no: int, index: int, note: str, root: Optional[str] = None
    ) -> None:
        position = self.fretboard.get_single_note_position(string_no, index)
        _note: Union[OpenNote, FrettedNote]
        if index == 0:
            _note = self._get_open_note(position, note, root)
        else:
            _note = self._get_fretted_note(position, note, root)
        self.elements.notes.append(_note)

    def add_note(self, string_no: int, note: str, root: Optional[str] = None) -> None:
        """Build and add background element."""
        if string_no < 0 or string_no > len(self.tuning):
            raise ValueError(f"String number is invalid. Tuning is {self.tuning}")

        # Note when fret == 0
        string_root = self.fretboard.get_list_in_good_order(self.tuning)[string_no]
        # Note when fret == N
        string_root = get_note_from_index(self.config.general.first_fret, string_root)
        # Index of the note from root
        _idx = chromatic_position_from_root(note, string_root)
        indices = []
        while _idx <= self.config.general.last_fret - self.config.general.first_fret:
            indices.append(_idx)
            _idx += 12

        for idx in indices:
            self._add_single_note(string_no, idx, note, root)

    def add_single_note_from_index(
        self, string_no: int, index: int, root: Optional[str] = None
    ) -> None:
        """Build and add background element."""
        string_note = self.tuning[string_no]
        note = get_note_from_index(index, string_note)

        self._add_single_note(string_no, index, note, root)

    def _add_cross_or_note(
        self, root: Optional[str], string_no: int, finger_position: Optional[int]
    ) -> None:
        if finger_position is None:
            position = self.fretboard.get_cross_position(string_no)
            cross = Cross(position, config=self.config.cross)
            self.elements.crosses.append(cross)
        else:
            string_note = get_note_from_index(
                finger_position,
                self.fretboard.get_list_in_good_order(self.tuning)[string_no],
            )
            if finger_position > 0:
                finger_position -= self.config.general.first_fret
                if finger_position <= 0:
                    return None

            self._add_single_note(string_no, finger_position, string_note, root)

    def add_notes(self, scale: NotesContainer) -> None:
        """Add an entire scale (from NoteContainer object) to the fretboard.

        Parameters
        ----------
        scale : NotesContainer
            Object representing the root and the associated scale
        """
        notes = scale.notes
        if self.config.general.enharmonic:
            notes = scale_to_enharmonic(scale.notes)
        for string_no, _ in enumerate(self.tuning):
            for note in notes:
                self.add_note(string_no, note, scale.root)

    def add_fingering(
        self, fingering: List[Optional[int]], root: Optional[str] = None
    ) -> None:
        """Add fingering starting with upper string to lower string.

        This function automatically calculate the note names or
        intervals if the root is given Display them in the way described
        in configuration
        """
        if len(fingering) != len(self.tuning):
            raise ValueError(
                f"Fingering has not the same size as tuning."
                f" Got {len(fingering)} expected {len(self.tuning)}"
            )
        for string_no, finger_position in enumerate(
            self.fretboard.get_list_in_good_order(fingering)
        ):
            self._add_cross_or_note(root, string_no, finger_position)

    def add_scale(
        self, scale: List[List[Optional[int]]], root: Optional[str] = None
    ) -> None:
        """Add scale starting with upper string to lower string.

        This function automatically calculate the note names or
        intervals if the root is given Display them in the way described
        in configuration
        """
        if len(scale) != len(self.tuning):
            raise ValueError(
                f"Scale has not the same size as tuning."
                f" Got {len(scale)} expected {len(self.tuning)}"
            )

        for string_no, finger_positions in enumerate(
            self.fretboard.get_list_in_good_order(scale)
        ):
            for finger_position in finger_positions:
                self._add_cross_or_note(root, string_no, finger_position)

    def add_note_element(self, note: Union[OpenNote, FrettedNote]) -> None:
        """Add a note element to the fretboard.

        Need to be either a OpenNote or a FrettedNote

        Parameters
        ----------
        note : Union[OpenNote, FrettedNote]
            Note element

        Raises
        ------
        ValueError
            If the note is not a Union[OpenNote, FrettedNote]
        """
        self.elements.notes.append(note)

    def add_element(self, element: FretBoardElement) -> None:
        """Add an element to the fretboard.

        Need to be either a FretBoardElement

        Parameters
        ----------
        element : FretBoardElement
            Fretboard element

        Raises
        ------
        ValueError
            If the element is not a FretboardElement
        """
        if not issubclass(type(element), FretBoardElement):
            raise ValueError("Element should be a 'FretBoardElement'")
        self.elements.customs.append(element)

    def get_elements(self) -> FretBoardElements:
        return self.elements

    def get_size(self) -> Tuple[float, float]:
        """Get total size of the drawing.

        Returns
        -------
        Tuple[float, float]
            Width and heigth
        """
        return self.fretboard.get_size()

    def get_inside_bounds(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Get the size of the inner drawing.

        This function could be use to add custom elements

        Returns
        -------
        Tuple[Tuple[float, float], Tuple[float, float]]
            Upper left corner x coordinate, upper left corner y coordinate
            Lower right corner x coordinate, lower right corner y coordinate
        """
        return self.fretboard.get_inside_bounds()

    def export(
        self, to: Union[Path, str], format: Literal["svg", "png", "pdf"] = "svg"
    ) -> None:
        """Export the fretboard to the desired path.

        Export availables are :
            svg
            png
            pdf

        Custom exporters can be created by :
        Subclassing : func:`~fretboardgtr.exporters.Exporter`
        Regitering it with func:`~fretboardgtr.exporters.register_exporter`

        Parameters
        ----------
        to : Union[Path, str]
            Path to export to
        format : Literal[&quot;svg&quot;, &quot;png&quot;, &quot;pdf&quot;], optional
            Format to export in, by default "svg"

        Raises
        ------
        NotImplementedError
            If the desired format is not implemented
        """
        to = Path(to)
        if format.upper() not in EXPORTERS:
            availables = ", ".join(list(EXPORTERS.keys()))
            raise NotImplementedError(
                f"Save to the {format} format is unsupported."
                f" Available formats are {availables}"
            )

        drawing = FretBoardToSVGConverter(self).convert()
        to.parent.mkdir(exist_ok=True)
        EXPORTERS[format.upper()](drawing).export(to=to)
