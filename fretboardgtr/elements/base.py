from abc import ABC, abstractmethod

import svgwrite


class FretBoardElement(ABC):
    """Interface to implement to define a FretBoard element.

    This simply consists of converting the element to a svgwrite element
    """

    @abstractmethod
    def get_svg(self) -> svgwrite.base.BaseElement:
        pass
