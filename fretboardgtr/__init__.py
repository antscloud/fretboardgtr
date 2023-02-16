"""Top-level package for FretBoardGtr."""
from fretboardgtr._version import version_str
from fretboardgtr.elements.background import Background, BackgroundConfig
from fretboardgtr.elements.fret_number import FretNumber, FretNumberConfig
from fretboardgtr.elements.frets import Fret, FretConfig
from fretboardgtr.elements.neck_dots import NeckDot, NeckDotConfig
from fretboardgtr.elements.notes import (
    FrettedNote,
    FrettedNoteConfig,
    OpenNote,
    OpenNoteConfig,
)
from fretboardgtr.elements.nut import Nut, NutConfig
from fretboardgtr.elements.strings import String, StringConfig
from fretboardgtr.elements.tuning import Tuning, TuningConfig
from fretboardgtr.fretboards.base import FretBoardLike
from fretboardgtr.fretboards.elements import FretBoardElements
from fretboardgtr.fretboards.fretboard import (
    FretBoardConfig,
    FretBoardContainer,
    FretBoardGeneralConfig,
)
from fretboardgtr.fretboards.svg_drawer import FretBoardToSVGConverter
from fretboardgtr.note_colors import NoteColors
from fretboardgtr.notes_creators import NotesContainer

__author__ = "Antoine Gibek"
__email__ = "antoine.gibek@gmail.com"
__version__ = version_str
