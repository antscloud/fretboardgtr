from dataclasses import dataclass
from typing import Optional, Tuple

import svgwrite

from fretboardgtr.base import ConfigIniter
from fretboardgtr.constants import BLACK, DARK_GRAY
from fretboardgtr.elements.base import FretBoardElement


@dataclass
class NeckDotConfig(ConfigIniter):
    """NeckDot element configuration."""

    color: str = DARK_GRAY
    color_stroke: str = BLACK
    width_stroke: int = 2
    radius: int = 7


class NeckDot(FretBoardElement):
    """Neck dots elements to be drawn in the final fretboard."""

    def __init__(
        self, position: Tuple[float, float], config: Optional[NeckDotConfig] = None
    ):
        self.config = config if config else NeckDotConfig()
        self.x = position[0]
        self.y = position[1]

    def get_svg(self) -> svgwrite.base.BaseElement:
        """Convert the NeckDot to a svgwrite object.

        This maps the NeckDotConfig configuration attributes to the svg
        attributes
        """
        circle = svgwrite.shapes.Circle(
            (self.x, self.y),
            r=self.config.radius,
            fill=self.config.color,
            stroke=self.config.color_stroke,
            stroke_width=self.config.width_stroke,
        )
        return circle
