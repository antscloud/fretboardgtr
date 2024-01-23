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

    def get_scale(self, tuning: List[str], max_spacing: int = 5) -> List[List[int]]:
        """Get the scale of each string in the given tuning.

        Goes from 0 up to (12 + max_spacing - 1) on the fretboard

        Parameters
        ----------
        tuning (List[str])
            The tuning of each string.

        Returns
        -------
        List[List[int]]
            The scale of each string in the tuning.
        """
        scale = []

        # Iterate over each string in the tuning
        for string_note in tuning:
            indices = []

            # Iterate over each note in the self.notes list
            for note in self.notes:
                _idx = chromatic_position_from_root(note, string_note)

                # Add the chromatic positions of the note on the string
                # until it reaches or exceeds the maximum position of 16
                while _idx <= 12 + max_spacing - 1:
                    indices.append(_idx)
                    _idx += 12

            # Sort the indices in ascending order
            scale.append(sorted(indices))

        return scale

    def get_chord_fingerings(
        self,
        tuning: List[str],
        max_spacing: int = 5,
        min_notes_in_chord: int = 2,
        number_of_fingers: int = 4,
    ) -> List[List[Optional[int]]]:
        """Get all probably possible fingering for a specific tuning.

        Parameters
        ----------
        tuning : List[str]
            List of note of the tuning
        max_spacing : int
            Maximum spacing between notes
        min_notes_in_chord : int
            Minimum number of notes in chord
        number_of_fingers : int
            Number of fingers allowed

        Returns
        -------
        List[List[Optional[int]]]
            List of propably possible fingerings
        """
        scale = self.get_scale(tuning, max_spacing)

        fingerings = []
        for combination in product(*scale):
            non_zero_numbers = [num for num in combination if num != 0]
            # No more than 4 fingers but duplicated allowed
            if len(set(non_zero_numbers)) > number_of_fingers:
                continue

            new_combination = list(combination)
            while True:
                # If 0 note or only one this is not a chord so break
                if len(non_zero_numbers) < min_notes_in_chord:
                    break
                # If the spacing is less than 5 then it'ok so break
                if max(non_zero_numbers) - min(non_zero_numbers) <= max_spacing:
                    break

                # If the spacing is more than 5 then remplace min values by None
                index_of_min = find_first_index(new_combination, min(non_zero_numbers))
                index_of_non_zero_min = find_first_index(
                    non_zero_numbers, min(non_zero_numbers)
                )
                if index_of_min is not None and index_of_non_zero_min is not None:
                    new_combination[index_of_min] = None
                    del non_zero_numbers[index_of_non_zero_min]

            notes = []
            for index, note in zip(new_combination, tuning):
                if index is not None:
                    notes.append(get_note_from_index(index, note))

            # Each notes should appear at least once.
            if set(notes) != set(self.notes):
                continue

            fingerings.append(list(new_combination))
        return fingerings

    def get_scale_positions(
        self,
        tuning: List[str],
        max_spacing: int = 5,
    ) -> List[List[List[Optional[int]]]]:
        """Get all possible scale positions for a specific tuning.

        Parameters
        ----------
        tuning : List[str]
            List of note of the tuning
        max_spacing : int
            Maximum spacing between notes

        Returns
        -------
        List[List[List[Optional[int]]]]
            List of all possible scale positions
        """
        scale = self.get_scale(tuning, max_spacing)
        fingerings: List[List[List[Optional[int]]]] = []
        for first_string_pos in scale[0]:
            fingering: List[List[Optional[int]]] = []
            for string in scale:
                string_fingering: List[Optional[int]] = []
                for note in string:
                    if (
                        note - first_string_pos < 0
                        or note - first_string_pos >= max_spacing
                    ):
                        continue
                    string_fingering.append(note)
                fingering.append(string_fingering)
            fingerings.append(fingering)
        return fingerings


class ScaleFromName:
    """Object that generating NotesContainer object from root and mode.

    Given a root name and a mode name, get the resulting scale.

    Also :
    Mode name can be given thanks to the constants.ModeName enum as well as string
    Note name can be given thanks to the constants.NoteName enum as well as string

    Example
    -------
    >>> ScaleFromName(root='C',mode='Dorian').build()
        NotesContainer(root= 'C', scale = ['C', 'D', 'D#', 'F', 'G', 'A', 'A#'])
    >>> ScaleFromName(root=Name.C,mode=ModeName.DORIAN).build()
        NotesContainer(root= 'C', scale = ['C', 'D', 'D#', 'F', 'G', 'A', 'A#'])
    """

    def __init__(self, root: str = "C", mode: str = "Ionian"):
        self.root = root
        self.mode = mode

    def build(self) -> NotesContainer:
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
    Mode name can be given thanks to the constants.ChordName enum as well as string
    Note name can be given thanks to the constants.NoteName enum as well as string

    Example
    -------
    >>> ChordFromName(root='C',quality='M').build()
        NotesContainer(root= 'C', scale = ['C', 'E', 'G'])
    >>> ChordFromName(root=NoteName.C,quality=ChordName.MAJOR).build()
        NotesContainer(root= 'C', scale = ['C', 'E', 'G'])
    """

    def __init__(self, root: str = "C", quality: str = "M"):
        self.root = root
        self.quality = quality

    def build(self) -> NotesContainer:
        index = CHROMATICS_NOTES.index(self.root)

        quality_idx = CHORDS_DICT_ESSENTIAL[self.quality]
        scale = []
        for note_id in quality_idx:
            scale.append(CHROMATICS_NOTES[(index + note_id) % 12])
        return NotesContainer(self.root, scale)
