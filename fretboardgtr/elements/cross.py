from dataclasses import dataclass
from typing import Optional, Tuple

from fretboardgtr.constants import BLACK

TEXT_OFFSET = "0.3em"
TEXT_STYLE = "text-anchor:middle"
import svgwrite

from fretboardgtr.base import ConfigIniter
from fretboardgtr.elements.base import FretBoardElement


@dataclass
class CrossConfig(ConfigIniter):
    color: str = BLACK
    fontsize: int = 35
    fontweight: str = "bold"


class Cross(FretBoardElement):
    def __init__(
        self,
        position: Tuple[float, float],
        config: Optional[CrossConfig] = None,
    ):
        self.config = config if config else CrossConfig()
        self.name = "X"
        self.x = position[0]
        self.y = position[1]

    def get_svg(self) -> svgwrite.base.BaseElement:
        text = svgwrite.text.Text(
            self.name,
            insert=(self.x, self.y),
            dy=[TEXT_OFFSET],
            font_size=self.config.fontsize,
            fill=self.config.color,
            font_weight=self.config.fontweight,
            style=TEXT_STYLE,
        )
        return text
