import mimetypes
import tempfile
from pathlib import Path

import pytest
import svgwrite
from PIL import Image
from pypdf import PdfReader

from fretboardgtr.exporters import PDFExporter, PNGExporter, SVGExporter


@pytest.fixture()
def drawing():
    dwg = svgwrite.Drawing(
        size=(  # +2 == Last fret + tuning
            100,
            100,
        ),
        profile="full",
    )
    circle = svgwrite.shapes.Circle(
        (50, 50),
        r=20,
    )
    dwg.add(circle)
    return dwg


def test_svg_exporter(drawing):
    svg_exporter = SVGExporter(drawing)
    with tempfile.TemporaryDirectory() as tmp_dir:
        outfile = Path(tmp_dir) / "tmp_file.svg"
        assert not outfile.exists()
        svg_exporter.export(outfile)
        assert outfile.exists()
        assert mimetypes.guess_type(outfile)[0] == "image/svg+xml"


def test_png_exporter(drawing):
    png_exporter = PNGExporter(drawing)
    with tempfile.TemporaryDirectory() as tmp_dir:
        outfile = Path(tmp_dir) / "tmp_file.png"
        assert not outfile.exists()
        png_exporter.export(outfile)
        assert outfile.exists()
        assert mimetypes.guess_type(outfile)[0] == "image/png"
        img = Image.open(outfile)
        assert img.format == "PNG"


def test_pdf_exporter(drawing):
    pdf_exporter = PDFExporter(drawing)
    with tempfile.TemporaryDirectory() as tmp_dir:
        outfile = Path(tmp_dir) / "tmp_file.pdf"
        assert not outfile.exists()
        pdf_exporter.export(outfile)
        assert outfile.exists()
        assert mimetypes.guess_type(outfile)[0] == "application/pdf"
        assert len(PdfReader(outfile).pages) == 1
