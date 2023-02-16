import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from dataclasses import dataclass

from fretboardgtr.base import ConfigIniter
from fretboardgtr.elements.background import BackgroundConfig
from fretboardgtr.elements.cross import CrossConfig
from fretboardgtr.elements.fret_number import FretNumberConfig
from fretboardgtr.elements.frets import FretConfig
from fretboardgtr.elements.neck_dots import NeckDotConfig
from fretboardgtr.elements.notes import FrettedNoteConfig, OpenNoteConfig
from fretboardgtr.elements.nut import NutConfig
from fretboardgtr.elements.strings import StringConfig
from fretboardgtr.elements.tuning import TuningConfig
from fretboardgtr.note_colors import NoteColors


@dataclass
class FretBoardGeneralConfig(ConfigIniter):
    x_start: float = 30.0
    y_start: float = 30.0
    x_end_offset: float = 0.0
    y_end_offset: float = 0.0
    fret_height: int = 50
    fret_width: int = 70
    first_fret: int = 0
    last_fret: int = 12
    show_tuning: bool = True
    show_frets: bool = True
    show_nut: bool = True
    show_degree_name: bool = False
    show_note_name: bool = True
    open_color_scale: bool = False
    fretted_color_scale: bool = True
    open_colors: NoteColors = NoteColors()
    fretted_colors: NoteColors = NoteColors()
    enharmonic: bool = True


@dataclass
class FretBoardConfig(ConfigIniter):
    general: FretBoardGeneralConfig = FretBoardGeneralConfig()
    background: BackgroundConfig = BackgroundConfig()
    fret_numbers: FretNumberConfig = FretNumberConfig()
    neck_dots: NeckDotConfig = NeckDotConfig()
    frets: FretConfig = FretConfig()
    nut: NutConfig = NutConfig()
    tuning: TuningConfig = TuningConfig()
    strings: StringConfig = StringConfig()
    open_notes: OpenNoteConfig = OpenNoteConfig()
    fretted_notes: FrettedNoteConfig = FrettedNoteConfig()
    cross: CrossConfig = CrossConfig()
