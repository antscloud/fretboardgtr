import os
from typing import List, Optional, Tuple

from fretboardgtr.constants import (
    ALTERATIONS,
    CHROMATICS_INTERVALS,
    CHROMATICS_NOTES,
    DOTS_FRETBOARD_POSITIONS,
    ENHARMONICS,
    NUMBER_OF_DOTS,
    SHARPY_ALTERATIONS,
)


def _contains_duplicates(l: list) -> bool:
    if len(l) != len(set(l)):
        return True
    return False


def chromatics_from_root(root: str) -> List[str]:
    """Create list of notes chromatically where the first element is the root"""
    notes: List[str] = [0] * len(CHROMATICS_NOTES)
    for j in range(len(CHROMATICS_NOTES)):
        notes[j] = CHROMATICS_NOTES[(CHROMATICS_NOTES.index(root) + j) % 12]
    return notes


def chromatic_position_from_root(note: str, root: str):
    chroma_from_root = chromatics_from_root(root)
    for idx, chromatic_note in enumerate(chroma_from_root):
        if chromatic_note == note:
            return idx
    return None


def to_sharp_note(note: str) -> str:
    if note in ALTERATIONS:
        note = ALTERATIONS[note]
    return note


def to_flat_note(note: str) -> str:
    if note in SHARPY_ALTERATIONS:
        note = SHARPY_ALTERATIONS[note]
    return note


def scale_to_sharp(scale: List[str]):
    flat_scale = list(scale)
    for i, note in enumerate(scale):
        sharp_note = to_sharp_note(note)
        flat_scale[i] = sharp_note
    return flat_scale


def scale_to_flat(scale: List[str]):
    flat_scale = list(scale)
    for i, note in enumerate(scale):
        sharp_note = to_flat_note(note)
        flat_scale[i] = sharp_note
    return flat_scale


def note_to_interval(note: str, root: str) -> int:
    sharp_note = to_sharp_note(note)
    idx = chromatic_position_from_root(sharp_note, root)
    return idx


def note_to_interval_name(note: str, root: str):
    idx = note_to_interval(note, root)
    return CHROMATICS_INTERVALS[idx]


def scale_to_intervals(scale: List[str], root: str):
    """
    >>> scale_to_intervals(scale=['C','E','G'],root='C')
    [1,3,5]
    """
    intervals = []
    for note in scale:
        intervals.append(note_to_interval(note, root))
    return intervals


def scale_to_enharmonic(scale: List[str]):
    """
    Function that modify the scale in order to not repeat note
    i.e. turns into enharmonic way if possible
    >>> setenharmonic(['A#', 'C', 'D', 'D#', 'F', 'G', 'A'])
        ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']
    >>> setenharmonic(["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"])
        ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    >>> setenharmonic(['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'F'])
        ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F']
    """

    sharp_scale = scale_to_sharp(scale)
    enharmonic_scale = list(sharp_scale)

    if _contains_duplicates(sharp_scale):
        for i, note in enumerate(sharp_scale):
            # len == 2 means there is an alteration
            if len(note) == 2:
                enharmonic_scale[i] = ENHARMONICS[note]

    # If there is still duplicate then remove transform B and F
    if _contains_duplicates(enharmonic_scale):
        if "B" in enharmonic_scale:
            enharmonic_scale[enharmonic_scale.index("B")] = ENHARMONICS["B"]
        elif "F" in enharmonic_scale:
            enharmonic_scale[enharmonic_scale.index("F")] = ENHARMONICS["F"]

    return enharmonic_scale


def fretboard_min_max(fingering: List[int]):
    """
    Return the min and the max of fingering without None and 0.
    FretBoardGtr.minmax()
    (2,3)
    """
    # Replace None by 0
    fret_fing = [0 if v == None else v for v in fingering]
    # Remove Negative numbers
    fret_fing = [v for v in fret_fing if v > 0]

    return min(v for v in fret_fing if v > 0), max(fret_fing)


def get_note_names(fingering: List[Optional[int]], tuning: List[Optional[str]]):
    """
    Give name of note on fret depends on tunings
    >>>FretBoardGtr.notesname(fingering=[0,3,2,0,None,0])
    ['E','C','E','G',None,'E']
    """

    notes = [0] * len(tuning)

    for i in range(0, len(tuning)):
        if fingering[i] == None:
            notes[i] = None
        else:
            ind = CHROMATICS_NOTES.index(tuning[i])
            notes[i] = CHROMATICS_NOTES[(ind + fingering[i]) % 12]

    return notes


def gap_distance(fingering: List[Optional[int]]):
    """
    return the gap between the max fret and the min fret
    3 if distance < 3
    >>> FretBoardGtr.dist(fingering=[0,3,2,0,None,0])
    1
    """
    mini, maxi = fretboard_min_max(fingering)
    gap = maxi - mini
    if gap < 3:
        gap = 3
    return gap


def get_dots_positions(fingering: List[Optional[int]]) -> List[Tuple[int, int]]:
    """Find where the dot on the fretboard are depending on the minimum fret
    If the first finger is on the 2rd fret (for example a B) and there is nothing beside the function return the folowwings lists:
    dot=[1,3]
    nbdot=[1,1]
    >>>F=FretBoardGtr()
    >>>tupledot=F.wheredot()
    ([2], [1])
    Because on the 3rd fret and the 5th
    That leads to put a dot on the second fret and the fourth fret corresponding to the third and a fifth on the guitar.
    """
    min_fret, _ = fretboard_min_max(fingering)
    gap_dist = gap_distance(fingering)

    dots = []
    if gap_dist >= 12:
        for i in range(1, (gap_dist // 12) * len(DOTS_FRETBOARD_POSITIONS)):
            DOTS_FRETBOARD_POSITIONS.append(DOTS_FRETBOARD_POSITIONS[i] + 12)
            NUMBER_OF_DOTS.append(NUMBER_OF_DOTS[i])

    for i in range(len(DOTS_FRETBOARD_POSITIONS)):
        if (
            DOTS_FRETBOARD_POSITIONS[i] >= (min_fret) % 12
            and DOTS_FRETBOARD_POSITIONS[i] < min_fret % 12 + gap_dist + 1
        ):
            dots.append((DOTS_FRETBOARD_POSITIONS[i] - min_fret % 12, NUMBER_OF_DOTS[i]))

    if min_fret == 0:
        dots.pop(0)

    return dots
