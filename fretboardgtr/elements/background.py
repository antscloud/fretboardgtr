from fretboardgtr.constants import GRAY
from dataclasses import dataclass
from typing import Tuple

import svgwrite
from typing import Optional
from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.base import ConfigIniter


@dataclass
class BackgroundConfig(ConfigIniter):
    color: str = GRAY
    opacity: float = 0.2


class Background(FretBoardElement):
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
        rectangle = svgwrite.shapes.Rect(
            insert=self.position,
            size=self.size,  # -2 evite case du bas du tuning
            rx=None,
            ry=None,
            fill=self.config.color,
            fill_opacity=self.config.opacity,
        )
        return rectangle
