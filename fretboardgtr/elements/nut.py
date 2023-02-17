from dataclasses import dataclass
from typing import Optional, Tuple

import svgwrite

from fretboardgtr.base import ConfigIniter
from fretboardgtr.constants import BLACK
from fretboardgtr.elements.base import FretBoardElement

SVG_OVERLAY = 10  # overlay


@dataclass
class NutConfig(ConfigIniter):
    """Nut element configuration."""

    color: str = BLACK
    width: int = 6


class Nut(FretBoardElement):
    """Nut element to be drawn in the final fretboard."""

    def __init__(
        self,
        start_position: Tuple[float, float],
        end_position: Tuple[float, float],
        config: Optional[NutConfig] = None,
    ):
        self.config = config if config else NutConfig()
        self.start_position = start_position
        self.end_position = end_position

    def get_svg(self) -> svgwrite.base.BaseElement:
        """Convert the Nut to a svgwrite object.

        This maps the NutConfig configuration attributes to the svg
        attributes
        """
        line = svgwrite.shapes.Line(
            start=self.start_position,
            end=self.end_position,
            stroke=self.config.color,
            stroke_width=self.config.width,
        )
        return line
