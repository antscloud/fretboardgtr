from dataclasses import dataclass
from typing import Optional, Tuple

from fretboardgtr.constants import BLACK, WHITE

TEXT_OFFSET = "0.3em"
TEXT_STYLE_PREFIX = "text-anchor:"
import svgwrite

from fretboardgtr.base import ConfigIniter
from fretboardgtr.elements.base import FretBoardElement

@dataclass
class TextConfig(ConfigIniter):
    """OpenNote element configuration."""

    color: str = WHITE
    stroke_color: str = BLACK
    stroke_width: int = 3
    text_color: str = BLACK
    fontsize: int = 30
    fontweight: str = "bold"

class Text(FretBoardElement):

    def __init__(
        self,
        text: str,
        position: Tuple[float,float],
        align: str = "middle",
        config: Optional[TextConfig] = None
    ):
        self.config = config if config else TextConfig() 
        self.text = text
        self.position = position
        self.align = align 

    def get_svg(self) -> svgwrite.base.BaseElement:
        """Convert the Nut to a svgwrite object.

        This maps the NutConfig configuration attributes to the svg
        attributes
        """
        text = svgwrite.text.Text(
            self.text,
            insert=self.position,
            dy=[TEXT_OFFSET],
            font_size=self.config.fontsize,
            fill=self.config.text_color,
            font_weight=self.config.fontweight,
            style=TEXT_STYLE_PREFIX+self.align,
        )
        return text