from dataclasses import dataclass, field, fields
from typing import List, Optional, Union

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


@dataclass
class FretBoardElements:
    """Container dataclass for the different elements of fretboards."""

    background: Optional[Background] = None
    fret_numbers: List[FretNumber] = field(default_factory=list)
    neck_dots: List[NeckDot] = field(default_factory=list)
    frets: List[Fret] = field(default_factory=list)
    nut: Optional[Nut] = None
    tuning: List[Tuning] = field(default_factory=list)
    strings: List[String] = field(default_factory=list)
    notes: List[Union[OpenNote, FrettedNote]] = field(default_factory=list)
    crosses: List[Cross] = field(default_factory=list)
    customs: List[FretBoardElement] = field(default_factory=list)

    def to_list(self) -> List[FretBoardElement]:
        """Convert the elements to a flat list of element."""
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
