import tempfile
import uuid
from pathlib import Path
from typing import Union

import svgwrite


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
        to = Path(to)
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = Path(tmp_dir) / Path(f"{uuid.uuid4()}.svg")
            self.drawing.saveas(str(tmp_file))

            drawing = svg2rlg(tmp_file)
            renderPM.drawToFile(drawing, str(to))


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
        to = Path(to)
        with tempfile.TemporaryDirectory() as tmp_dir:
            tmp_file = Path(tmp_dir) / Path(f"{uuid.uuid4()}.svg")
            self.drawing.saveas(str(tmp_file))

            drawing = svg2rlg(tmp_file)
            renderPDF.drawToFile(drawing, str(to))
