from fretboardgtr.constants import BLACK, DARK_GRAY
from dataclasses import dataclass
from typing import Tuple
from typing import Optional
import svgwrite
from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.base import ConfigIniter


@dataclass
class NeckDotConfig(ConfigIniter):
    color: str = DARK_GRAY
    color_stroke: str = BLACK
    width_stroke: int = 2
    radius: int = 7


class NeckDot(FretBoardElement):
    def __init__(
        self, position: Tuple[float, float], config: Optional[NeckDotConfig] = None
    ):
        self.config = config if config else NeckDotConfig()
        self.x = position[0]
        self.y = position[1]

    def get_svg(self) -> svgwrite.base.BaseElement:
        circle = svgwrite.shapes.Circle(
            (self.x, self.y),
            r=self.config.radius,
            fill=self.config.color,
            stroke=self.config.color_stroke,
            stroke_width=self.config.width_stroke,
        )
        return circle
