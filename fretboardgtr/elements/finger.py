from dataclasses import dataclass
from typing import Optional, Tuple

from fretboardgtr.constants import BLACK, WHITE

TEXT_OFFSET = "0.3em"
TEXT_STYLE = "text-anchor:middle"
import svgwrite

from fretboardgtr.base import ConfigIniter
from fretboardgtr.elements.base import FretBoardElement

@dataclass
class FingerConfig(ConfigIniter):
    radius: int = 23
    color: str = BLACK
    stroke_color: str = BLACK
    stroke_width: int = 3
    text_color: str = WHITE
    fontsize: int = 20
    fontweight: str = "bold"


class Finger(FretBoardElement):
    """Finger elements to be drawn in the final fretboard."""

    def __init__(
        self,
        position: Tuple[float, float],
        size: Tuple[float, float],
        text: str,
        config: Optional[FingerConfig] = None,
    ):
        self.config = config if config else FingerConfig()
        self.pos = position
        self.size = size
        self.text = text

    def get_svg(self) -> svgwrite.base.BaseElement:
        """Convert the Finger to a svgwrite object.

        This maps the FingerConfig configuration attributes to the
        svg attributes
        """
        finger = svgwrite.container.Group()

        rect = svgwrite.shapes.Rect(
            self.pos,
            self.size,
            rx=self.config.radius,
            ry=self.config.radius,
            fill=self.config.color,
            stroke=self.config.stroke_color,
            stroke_width=self.config.stroke_width,
        )

        text = svgwrite.text.Text(
            self.text,
            insert=(self.pos[0] + self.size[0]/2, self.pos[1]+self.size[1]/2),
            dy=[TEXT_OFFSET],
            font_size=self.config.fontsize,
            fill=self.config.text_color,
            font_weight="bold",
            style=TEXT_STYLE,
        )

        finger.add(rect)
        finger.add(text)
        return finger