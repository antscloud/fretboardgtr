from dataclasses import fields

import svgwrite

from fretboardgtr.elements.base import FretBoardElement
from fretboardgtr.fretboards.base import FretBoardLike


class FretBoardToSVGConverter:
    """Convert a FretboardLike object to a svgwrite object.

    Convert it in order to export it to a specific format later.
    """

    def __init__(self, fretboard: FretBoardLike):
        self._fretboard = fretboard
        self.drawing = self.get_empty()

    def get_empty(self) -> svgwrite.Drawing:
        """Create empty box and the object self.drawing."""
        width, height = self._fretboard.get_size()
        return svgwrite.Drawing(
            size=(width, height),
            profile="full",
        )

    def add_to_drawing(
        self, drawing: svgwrite.Drawing, element: FretBoardElement
    ) -> svgwrite.Drawing:
        if not issubclass(type(element), FretBoardElement):
            raise ValueError(f"Element {element} does not subclass FretBoardElement")
        drawing.add(element.get_svg())
        return drawing

    def convert(self) -> svgwrite.Drawing:
        drawing = self.get_empty()
        elements = self._fretboard.get_elements()
        for key in fields(elements):
            element = getattr(elements, key.name, None)
            if isinstance(element, list):
                for sub in element:
                    drawing = self.add_to_drawing(drawing, sub)
            else:
                drawing = self.add_to_drawing(drawing, element)  # type: ignore
        return drawing
