from dataclasses import dataclass

from fretboardgtr.constants import INTERVAL_MAPPING, WHITE

TEXT_OFFSET = "0.3em"
TEXT_STYLE = "text-anchor:middle"
from fretboardgtr.base import ConfigIniter


@dataclass
class NoteColors(ConfigIniter):
    root: str = "rgb(231, 0, 0)"
    minorsecond: str = "rgb(249, 229, 0)"
    majorsecond: str = "rgb(249, 165, 0)"
    minorthird: str = "rgb(0, 94, 0)"
    majorthird: str = "rgb(0, 108, 0)"
    perfectfourth: str = "rgb(0, 154, 0)"
    diminishedfifth: str = "rgb(0, 15, 65)"
    perfectfifth: str = "rgb(0, 73, 151)"
    minorsixth: str = "rgb(168, 107, 98)"
    majorsixth: str = "rgb(222, 81, 108)"
    minorseventh: str = "rgb(120, 37, 134)"
    majorseventh: str = "rgb(120, 25, 98)"

    def from_short_interval(self, interval: str) -> str:
        color = WHITE
        for long, short in INTERVAL_MAPPING.items():
            if interval != short:
                continue
            if hasattr(self, long):
                color = getattr(self, long)
        return color

    def from_interval(self, interval: int) -> str:
        cls_keys = list(self.__annotations__)
        color = getattr(self, cls_keys[interval % 12])
        return color
