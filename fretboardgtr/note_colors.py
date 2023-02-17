from dataclasses import dataclass

from fretboardgtr.constants import INTERVAL_MAPPING, WHITE

TEXT_OFFSET = "0.3em"
TEXT_STYLE = "text-anchor:middle"
from fretboardgtr.base import ConfigIniter


@dataclass
class NoteColors(ConfigIniter):
    """Dataclass containing the mapping of colors and intervals."""

    root: str = "rgb(231, 0, 0)"
    minor_second: str = "rgb(249, 229, 0)"
    major_second: str = "rgb(249, 165, 0)"
    minor_third: str = "rgb(0, 94, 0)"
    major_third: str = "rgb(0, 108, 0)"
    perfect_fourth: str = "rgb(0, 154, 0)"
    diminished_fifth: str = "rgb(0, 15, 65)"
    perfect_fifth: str = "rgb(0, 73, 151)"
    minor_sixth: str = "rgb(168, 107, 98)"
    major_sixth: str = "rgb(222, 81, 108)"
    minor_seventh: str = "rgb(120, 37, 134)"
    major_seventh: str = "rgb(120, 25, 98)"

    def from_short_interval(self, interval: str) -> str:
        """Get color for the given short interval.

        Parameters
        ----------
        interval : str
            String representing the interval

        Returns
        -------
        str
            RGB color as string

        Example
        -------
        from fretboardgtr.constants import Interval
        >>> NoteColors().from_short_interval(Interval.MINOR_SIXTH)
            "rgb(168, 107, 98)"
        """
        color = WHITE
        for long, short in INTERVAL_MAPPING.items():
            if interval != short:
                continue
            if hasattr(self, long):
                color = getattr(self, long)
        return color

    def from_interval(self, interval: int) -> str:
        """Get color for the given long interval name.

        Parameters
        ----------
        interval : str
            String representing the long interval

        Returns
        -------
        str
            RGB color as string

        Example
        -------
        from fretboardgtr.constants import LongInterval
        >>> NoteColors().from_short_interval(LongInterval.MINOR_SIXTH)
            "rgb(168, 107, 98)"
        """
        cls_keys = list(self.__annotations__)
        color = getattr(self, cls_keys[interval % 12])
        return color
