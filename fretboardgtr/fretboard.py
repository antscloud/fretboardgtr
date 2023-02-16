import os
import sys
from pathlib import Path
from typing import List, Literal, Tuple, Union

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from typing import Optional

from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.elements.notes import FrettedNote, OpenNote
from fretboardgtr.exporters import EXPORTERS
from fretboardgtr.fretboards.base import FretBoardLike
from fretboardgtr.fretboards.fretboard import FretBoardConfig, FretBoardContainer
from fretboardgtr.fretboards.svg_drawer import FretBoardToSVGConverter
from fretboardgtr.fretboards.vertical import VerticalFretBoardContainer
from fretboardgtr.notes_creators import NotesContainer


class FretBoard:
    def __init__(
        self,
        tuning: Optional[List[str]] = None,
        config: Optional[FretBoardConfig] = None,
    ):
        self._fretboard: FretBoardLike = FretBoardContainer(
            config=config, tuning=tuning
        )

    def set_config(self, config: FretBoardConfig) -> None:
        if not issubclass(type(config), FretBoardConfig):
            raise ValueError(f"scale should be a FretBoardConfig nor {type(config)}")
        self._fretboard.set_config(config)

    def add_notes(self, scale: NotesContainer) -> None:
        if not issubclass(type(scale), NotesContainer):
            raise ValueError(f"scale should be a NotesContainer nor {type(scale)}")
        self._fretboard.add_scale(scale=scale)

    def add_fingering(self, fingering: List[Optional[int]]) -> None:
        self._fretboard.add_fingering(fingering=fingering)

    def add_note_element(self, note: Union[OpenNote, FrettedNote]) -> None:
        self._fretboard.add_note_element(note)

    def add_element(self, element: FretBoardElement) -> None:
        self._fretboard.add_element(element)

    def get_inside_bounds(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        return self._fretboard.get_inside_bounds()

    def export(
        self, to: Union[Path, str], format: Literal["svg", "png", "pdf"] = "svg"
    ) -> None:
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


def main():
    from fretboardgtr.notes_creators import ScaleFromName

    fretboard = FretBoard()
    c_major = ScaleFromName(root="C", mode="Ionian").get()
    fretboard.add_notes(scale=c_major)
    fretboard.export("c_ionian.svg")


if __name__ == "__main__":
    main()
