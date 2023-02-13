from dataclasses import dataclass
from typing import Optional, Tuple

import svgwrite

from fretboardgtr.base import ConfigIniter
from fretboardgtr.constants import GRAY
from fretboardgtr.elements.base import FretBoardElement

SVG_OVERLAY = 10  # overlay


@dataclass
class FretConfig(ConfigIniter):
    color: str = GRAY
    width: int = 3


class Fret(FretBoardElement):
    def __init__(
        self,
        start_position: Tuple[float, float],
        end_position: Tuple[float, float],
        config: Optional[FretConfig] = None,
    ):
        self.config = config if config else FretConfig()
        self.start_position = start_position
        self.end_position = end_position

    def get_svg(self) -> svgwrite.base.BaseElement:
        line = svgwrite.shapes.Line(
            start=self.start_position,
            end=self.end_position,
            stroke=self.config.color,
            stroke_width=self.config.width,
        )
        return line
