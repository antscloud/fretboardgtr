import tempfile
import uuid
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Type, Union

import svgwrite


class Exporter(ABC):
    def __init__(self, drawing: svgwrite.Drawing):
        self.drawing = drawing

    @abstractmethod
    def export(self, to: Union[str, Path]):
        pass


class SVGExporter(Exporter):
    def export(self, to: Union[str, Path]):
        to = Path(to)
        self.drawing.saveas(str(to))


class PNGExporter(Exporter):
    def export(self, to: Union[str, Path]):
        try:
            from reportlab.graphics import renderPM
        except ImportError:
            raise ImportError(
                "Cannot export svg to PNG because reportlab package is missing"
            )
        try:
            from svglib.svglib import svg2rlg
        except ImportError:
            raise ImportError(
                "Cannot export svg to PNG because svglib package is missing"
            )
        to = Path(to)
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = Path(tmp_dir) / Path(f"{uuid.uuid4()}.svg")
            self.drawing.saveas(str(tmp_file))
            drawing = svg2rlg(str(tmp_file))
            renderPM.drawToFile(drawing, str(to))


class PDFExporter(Exporter):
    def export(self, to: Union[str, Path]):
        try:
            from reportlab.graphics import renderPDF
        except ImportError:
            raise ImportError(
                "Cannot export svg to PNG because reportlab package is missing"
            )
        try:
            from svglib.svglib import svg2rlg
        except ImportError:
            raise ImportError(
                "Cannot export svg to PNG because svglib package is missing"
            )
        to = Path(to)
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = Path(tmp_dir) / Path(f"{uuid.uuid4()}.svg")
            self.drawing.saveas(str(tmp_file))

            drawing = svg2rlg(str(tmp_file))
            renderPDF.drawToFile(drawing, str(to))


def register_exporter(exporter: Type[Exporter], extension: str):
    EXPORTERS[extension.upper()] = exporter


EXPORTERS: Dict[str, Type[Exporter]] = {}

register_exporter(SVGExporter, "SVG")
register_exporter(PNGExporter, "PNG")
register_exporter(PDFExporter, "PDF")
