from dataclasses import dataclass
from typing import List

from fretboardgtr.constants import CHORDS_DICT_ESSENTIAL, CHROMATICS_NOTES, SCALES_DICT


@dataclass
class NotesContainer:
    root: str
    notes: List[str]


class ScaleFromName:
    """Object that generating note container from root and mode.

    >>> ScaleFromName(root='C',mode='Dorian').results
        {'root': 'C', 'scale': ['C', 'D', 'D#', 'F', 'G', 'A', 'A#']}
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
    """Object that generating note container from root and quality.

    >>> ChordFromName(root='C',quality='M').results
        {'root': 'C', 'scale': ['C', 'E', 'G']}
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
