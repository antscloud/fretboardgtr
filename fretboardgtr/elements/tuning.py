from dataclasses import dataclass
from typing import Optional, Tuple

import svgwrite

from fretboardgtr.base import ConfigIniter
from fretboardgtr.constants import GRAY
from fretboardgtr.elements.base import FretBoardElement

TEXT_OFFSET = "0.3em"
TEXT_STYLE = "text-anchor:middle"


@dataclass
class TuningConfig(ConfigIniter):
    """Tuning element configuration."""

    color: str = GRAY
    fontsize: int = 20
    fontweight: str = "normal"


class Tuning(FretBoardElement):
    """Tuning texts elements to be drawn in the final fretboard."""

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
        """Convert the Tuning to a svgwrite object.

        This maps the TuningConfig configuration attributes to the svg
        attributes
        """
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
