from dataclasses import dataclass
from typing import Optional, Tuple

import svgwrite

from fretboardgtr.base import ConfigIniter
from fretboardgtr.constants import NO_COLOR
from fretboardgtr.elements.base import FretBoardElement


@dataclass
class BackgroundConfig(ConfigIniter):
    """Background element configuration."""

    color: str = NO_COLOR
    opacity: float = 0.7


class Background(FretBoardElement):
    """Background element to be drawn in the final fretboard."""

    def __init__(
        self,
        position: Tuple[float, float],
        size: Tuple[float, float],
        config: Optional[BackgroundConfig] = None,
    ):
        self.config = config if config else BackgroundConfig()
        self.position = position
        self.size = size

    def get_svg(self) -> svgwrite.base.BaseElement:
        """Convert the Background to a svgwrite object.

        This maps the BackgroundConfig configuration attributes to the
        svg attributes
        """
        rectangle = svgwrite.shapes.Rect(
            insert=self.position,
            size=self.size,  # -2 evite case du bas du tuning
            rx=None,
            ry=None,
            fill=self.config.color,
            fill_opacity=self.config.opacity,
        )
        return rectangle
