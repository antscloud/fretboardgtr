from abc import ABC, abstractmethod
from typing import List, Optional, Tuple, Union

from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.elements.notes import FrettedNote, OpenNote
from fretboardgtr.fretboards.config import FretBoardConfig
from fretboardgtr.fretboards.elements import FretBoardElements
from fretboardgtr.notes_creators import NotesContainer


class FretBoardLike(ABC):
    @abstractmethod
    def set_config(self, config: FretBoardConfig) -> None:
        pass

    @abstractmethod
    def add_note_element(self, note: Union[OpenNote, FrettedNote]) -> None:
        pass

    @abstractmethod
    def add_element(self, element: FretBoardElement) -> None:
        pass

    @abstractmethod
    def add_fingering(
        self, fingering: List[Optional[int]], root: Optional[str] = None
    ) -> None:
        pass

    @abstractmethod
    def add_scale(self, scale: NotesContainer) -> None:
        pass

    @abstractmethod
    def get_size(self) -> Tuple[float, float]:
        pass

    @abstractmethod
    def get_inside_bounds(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        pass

    @abstractmethod
    def get_elements(self) -> FretBoardElements:
        pass
