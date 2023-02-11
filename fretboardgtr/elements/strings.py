from fretboardgtr.constants import GRAY
from dataclasses import dataclass
from typing import Tuple, Optional
from fretboardgtr.constants import BLACK
import svgwrite
from typing import Optional
from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.elements.base import FretBoardElement, ConfigIniter


@dataclass
class StringConfig(ConfigIniter):
    color: str = BLACK
    width: int = 3


class String(FretBoardElement):
    def __init__(
        self,
        start_position: Tuple[float, float],
        end_position: Tuple[float, float],
        width: Optional[int] = None,
        config: Optional[StringConfig] = None,
    ):
        self.config = config if config else StringConfig()
        self.start_position = start_position
        self.end_position = end_position
        self.width = width

    def get_svg(self) -> svgwrite.base.BaseElement:
        if self.width is None:
            self.width = self.config.width

        line = svgwrite.shapes.Line(
            start=self.start_position,
            end=self.end_position,
            stroke=self.config.color,
            stroke_width=self.width,
        )
        return line