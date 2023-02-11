from fretboardgtr.constants import GRAY
from dataclasses import dataclass
from typing import Tuple
from typing import Optional
import svgwrite
from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.elements.base import FretBoardElement, ConfigIniter

TEXT_OFFSET = "0.3em"
TEXT_STYLE = "text-anchor:middle"


@dataclass
class TuningConfig(ConfigIniter):
    color: str = GRAY
    fontsize: int = 20
    fontweight: str = "normal"


class Tuning(FretBoardElement):
    def __init__(
        self,
        name: str,
        position: Tuple[float, float],
        config: Optional[TuningConfig] = None,
    ):
        self.config = config if config else TuningConfig()
        self.name = name
        self.x = position[0]
        self.y = position[1]

    def get_svg(self) -> svgwrite.base.BaseElement:
        text = svgwrite.text.Text(
            self.name,
            insert=(self.x, self.y),
            dy=[TEXT_OFFSET],
            fill=self.config.color,
            font_size=self.config.fontsize,
            font_weight=self.config.fontweight,
            style=TEXT_STYLE,
        )
        return text
