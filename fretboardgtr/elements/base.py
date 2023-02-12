from abc import ABC, abstractmethod
import svgwrite


class FretBoardElement(ABC):
    @abstractmethod
    def get_svg(self) -> svgwrite.base.BaseElement:
        pass
