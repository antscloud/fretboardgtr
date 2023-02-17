from dataclasses import dataclass
from typing import List

from fretboardgtr.constants import CHORDS_DICT_ESSENTIAL, CHROMATICS_NOTES, SCALES_DICT


@dataclass
class NotesContainer:
    root: str
    notes: List[str]


class ScaleFromName:
    """Object that generating NotesContainer object from root and mode.

    Given a root name and a mode name, get the resulting scale.

    Also :
    Mode name can be given thanks to the constants.Mode enum as well as string
    Note name can be given thanks to the constants.Note enum as well as string

    Example
    -------
    >>> ScaleFromName(root='C',mode='Dorian').get()
        NotesContainer(root= 'C', scale = ['C', 'D', 'D#', 'F', 'G', 'A', 'A#'])
    >>> ScaleFromName(root=Note.C,mode=Mode.DORIAN).get()
        NotesContainer(root= 'C', scale = ['C', 'D', 'D#', 'F', 'G', 'A', 'A#'])
    """

    def __init__(self, root: str = "C", mode: str = "Ionian"):
        self.root = root
        self.mode = mode

    def get(self) -> NotesContainer:
        index = CHROMATICS_NOTES.index(self.root)
        mode_idx = SCALES_DICT[self.mode]
        scale = []
        for note_id in mode_idx:
            scale.append(CHROMATICS_NOTES[(index + note_id) % 12])
        return NotesContainer(self.root, scale)


class ChordFromName:
    """Object generating NotesContainer object from root and chord quality.

    Given a root name and a quality name, get the resulting scale.

    Also :
    Mode name can be given thanks to the constants.Chord enum as well as string
    Note name can be given thanks to the constants.Note enum as well as string

    Example
    -------
    >>> ScaleFromName(root='C',quality='M).get()
        NotesContainer(root= 'C', scale = ['C', 'E', 'G'])
    >>> ScaleFromName(root=Note.C,quality=Chord.MAJOR).resultget()
        NotesContainer(root= 'C', scale = ['C', 'E', 'G'])
    """

    def __init__(self, root: str = "C", quality: str = "M"):
        self.root = root
        self.quality = quality

    def get(self) -> NotesContainer:
        index = CHROMATICS_NOTES.index(self.root)

        quality_idx = CHORDS_DICT_ESSENTIAL[self.quality]
        scale = []
        for note_id in quality_idx:
            scale.append(CHROMATICS_NOTES[(index + note_id) % 12])
        return NotesContainer(self.root, scale)
