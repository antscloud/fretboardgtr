from pathlib import Path
from typing import List, Literal, Optional, Tuple, Union

from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.elements.notes import FrettedNote, OpenNote
from fretboardgtr.exporters import EXPORTERS
from fretboardgtr.fretboards.base import FretBoardLike
from fretboardgtr.fretboards.converters import FretBoardToSVGConverter
from fretboardgtr.fretboards.fretboard import FretBoardConfig, FretBoardContainer
from fretboardgtr.fretboards.vertical import VerticalFretBoardContainer
from fretboardgtr.notes_creators import NotesContainer


class FretBoard:
    """High level API class for fretboard generation."""

    def __init__(
        self,
        tuning: Optional[List[str]] = None,
        config: Optional[FretBoardConfig] = None,
    ):
        self._fretboard: FretBoardLike = FretBoardContainer(
            config=config, tuning=tuning
        )

    def set_config(self, config: FretBoardConfig) -> None:
        """Set a new configuration for the fretboard.

        Changing the configuration does not affect elements already
        defined. Only new ones will be changed. If you want to change
        completely the fretboard from configuration, a new object should
        be created
        """
        if not issubclass(type(config), FretBoardConfig):
            raise ValueError(f"scale should be a FretBoardConfig nor {type(config)}")
        self._fretboard.set_config(config)

    def add_notes(self, scale: NotesContainer) -> None:
        """Add an entire scale (from NoteContainer object) to the fretboard.

        See :func:`~fretboardgtr.fretboards.fretboard.add_notes`
        """
        if not issubclass(type(scale), NotesContainer):
            raise ValueError(f"scale should be a NotesContainer nor {type(scale)}")
        self._fretboard.add_notes(scale=scale)

    def add_fingering(self, fingering: List[Optional[int]]) -> None:
        """Add fingering starting with upper string to lower string.

        See :func:`~fretboardgtr.fretboards.fretboard.add_fingering`
        """
        self._fretboard.add_fingering(fingering=fingering)

    def add_note_element(self, note: Union[OpenNote, FrettedNote]) -> None:
        """Add a note element to the fretboard.

        See :func:`~fretboardgtr.fretboards.fretboard.add_note_element`
        """
        self._fretboard.add_note_element(note)

    def add_element(self, element: FretBoardElement) -> None:
        """Add an element to the fretboard.

        See :func:`~fretboardgtr.fretboards.fretboard.add_element`
        """
        self._fretboard.add_element(element)

    def get_inside_bounds(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Get inside bounds of the fretboard.

        See :func:`~fretboardgtr.fretboards.fretboard.get_inside_bounds`
        """
        return self._fretboard.get_inside_bounds()

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
        if format.upper() not in EXPORTERS:
            availables = ", ".join(list(EXPORTERS.keys()))
            raise NotImplementedError(
                f"Save to the {format} format is unsupported."
                f" Available formats are {availables}"
            )
        drawing = FretBoardToSVGConverter(self._fretboard).convert()
        EXPORTERS[format.upper()](drawing).export(to=to)


class VerticalFretBoard(FretBoard):
    def __init__(
        self,
        tuning: Optional[List[str]] = None,
        config: Optional[FretBoardConfig] = None,
    ):
        self._fretboard: FretBoardLike = VerticalFretBoardContainer(
            config=config, tuning=tuning
        )

    def add_notes(self, scale: NotesContainer) -> None:
        """Add an entire scale (from NoteContainer object) to the fretboard.

        See :func:`~fretboardgtr.fretboards.vertical.add_notes`
        """
        super().add_notes(scale)

    def add_fingering(self, fingering: List[Optional[int]]) -> None:
        """Add fingering starting with upper string to lower string.

        See :func:`~fretboardgtr.fretboards.vertical.add_fingering`
        """
        super().add_fingering(fingering=fingering)

    def add_note_element(self, note: Union[OpenNote, FrettedNote]) -> None:
        """Add a note element to the fretboard.

        See :func:`~fretboardgtr.fretboards.vertical.add_note_element`
        """
        super().add_note_element(note)

    def add_element(self, element: FretBoardElement) -> None:
        """Add an element to the fretboard.

        See :func:`~fretboardgtr.fretboards.vertical.add_element`
        """
        super().add_element(element)

    def get_inside_bounds(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Get inside bounds of the fretboard.

        See :func:`~fretboardgtr.fretboards.vertical.get_inside_bounds`
        """
        return super().get_inside_bounds()
