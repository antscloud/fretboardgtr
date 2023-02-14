"""Script allowing creation of plot when building the docs.

You can then access to your plot through the docs. For doing this, the
make_plots function is called in the conf.py directory.
"""
import os

BASE_DIR = os.path.dirname(__file__)
EXPORT_FOLDER = os.path.join(BASE_DIR, "..", "source", "assets", "plots")


def doc_plot() -> None:
    """doc_plot Generate plot when building docs.

    Save it in EXPORT_FOLDER.
    """
    ...


def make_plots() -> None:
    os.makedirs(EXPORT_FOLDER, exist_ok=True)
    doc_plot()


if __name__ == "__main__":
    make_plots()
