from pathlib import Path
from typing import Union
import svgwrite
import uuid

import tempfile


class SVGExporter:
    def __init__(self, drawing: svgwrite.Drawing):
        self.drawing = drawing

    def export(self, to: Union[str, Path]):
        to = Path(to)
        self.drawing.saveas(str(to))


class PNGExporter:
    def __init__(self, drawing: svgwrite.Drawing):
        self.drawing = drawing

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

        tmp_file = Path(tempfile.TemporaryDirectory().name) / Path(
            f"{uuid.uuid4()}.svg"
        )
        self.drawing.saveas(str(tmp_file))

        drawing = svg2rlg(tmp_file)
        renderPM.drawToFile(drawing, to)


class PDFExporter:
    def __init__(self, drawing: svgwrite.Drawing):
        self.drawing = drawing

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

        tmp_file = Path(tempfile.TemporaryDirectory().name) / Path(
            f"{uuid.uuid4()}.svg"
        )
        self.drawing.saveas(str(tmp_file))

        drawing = svg2rlg(tmp_file)
        renderPDF.drawToFile(drawing, to)
