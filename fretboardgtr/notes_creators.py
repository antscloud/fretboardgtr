from dataclasses import dataclass
from itertools import product
from typing import List, Optional

from fretboardgtr.constants import CHORDS_DICT_ESSENTIAL, CHROMATICS_NOTES, SCALES_DICT
from fretboardgtr.utils import chromatic_position_from_root, get_note_from_index


def find_first_index(_list: List[int], value: int) -> Optional[int]:
    try:
        index = _list.index(value)
        return index
    except ValueError:
        return None  # If the value is not found in the tuple, return None


@dataclass
class NotesContainer:
    root: str
    notes: List[str]

    def get_probablely_possible_fingering(
        self, tuning: List[str]
    ) -> List[List[Optional[int]]]:
        """Get all probably possible fingering for a specific tuning.

        Parameters
        ----------
        tuning : List[str]
            List of note of the tuning

        Returns
        -------
        List[List[Optional[int]]]
            List of propably possible fingerings
        """
        scale = []
        for string_note in tuning:
            indices = []
            for note in self.notes:
                _idx = chromatic_position_from_root(note, string_note)
                while _idx <= 16:
                    indices.append(_idx)
                    _idx += 12
            scale.append(sorted(indices))

        fingerings = []
        for combination in product(*scale):
            non_zero_numbers = [num for num in combination if num != 0]

            # No more than 4 fingers but duplicated allowed
            if len(set(non_zero_numbers)) > 4:
                continue

            # No more than 5 frets spacing
            # else try to remplace min values by None
            # TODO: Also add the max checking
            new_combination = list(combination)

            while True:
                index_of_min = find_first_index(new_combination, min(non_zero_numbers))
                index_of_min_of_non_zero = find_first_index(
                    non_zero_numbers, min(non_zero_numbers)
                )

                if index_of_min is not None and index_of_min_of_non_zero is not None:
                    new_combination[index_of_min] = None
                    del non_zero_numbers[index_of_min_of_non_zero]

                if len(non_zero_numbers) < 2:
                    break

                if max(non_zero_numbers) - min(non_zero_numbers) <= 5:
                    break

            notes = []
            for index, note in zip(new_combination, tuning):
                if index is not None:
                    notes.append(get_note_from_index(index, note))

            # Each notes should appear at least once.
            if set(notes) != set(self.notes):
                continue
            fingerings.append(list(new_combination))
        return fingerings


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
    >>> ChordFromName(root='C',quality='M').get()
        NotesContainer(root= 'C', scale = ['C', 'E', 'G'])
    >>> ChordFromName(root=Note.C,quality=Chord.MAJOR).resultget()
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
