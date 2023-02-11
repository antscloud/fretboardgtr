from fretboardgtr.constants import BLACK
from dataclasses import dataclass
from typing import Tuple
from typing import Optional
import svgwrite
from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.elements.base import FretBoardElement, ConfigIniter

SVG_OVERLAY = 10  # overlay


@dataclass
class NutConfig(ConfigIniter):
    color: str = BLACK
    width: int = 6


class Nut(FretBoardElement):
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
        line = svgwrite.shapes.Line(
            start=self.start_position,
            end=self.end_position,
            stroke=self.config.color,
            stroke_width=self.config.width,
        )
        return line
