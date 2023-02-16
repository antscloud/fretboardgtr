from typing import Collection, List

from fretboardgtr.constants import (
    ALTERATIONS,
    CHROMATICS_INTERVALS,
    CHROMATICS_NOTES,
    DOTS_POSITIONS,
    ENHARMONICS,
    SHARPY_ALTERATIONS,
)


def get_valid_dots(first_fret: int, last_fret: int) -> List[int]:
    dots = []
    for dot in DOTS_POSITIONS:
        if dot >= first_fret and dot <= last_fret:
            dots.append(dot)
    return dots


def _contains_duplicates(iterable: Collection) -> bool:
    if len(iterable) != len(set(iterable)):
        return True
    return False


def chromatics_from_root(root: str) -> List[str]:
    """Create list of notes chromatically starting with root."""
    notes = []
    root_idx = CHROMATICS_NOTES.index(root)
    for i, _ in enumerate(CHROMATICS_NOTES):
        notes.append(CHROMATICS_NOTES[(root_idx + i) % 12])
    return notes


def get_note_from_index(index: int, root: str) -> str:
    """Get note from chromatic scale from index and root."""
    chroma_from_root = chromatics_from_root(root)
    return chroma_from_root[index % 12]


def chromatic_position_from_root(note: str, root: str) -> int:
    """Get the index of the note from the root on chromatic scale."""
    idx = 0
    chroma_from_root = chromatics_from_root(root)
    for _idx, chromatic_note in enumerate(chroma_from_root):
        if chromatic_note == note:
            idx = _idx
    return idx


def to_sharp_note(note: str) -> str:
    """Get note by replacing it by its corresponding sharp note."""
    if note in ALTERATIONS:
        note = ALTERATIONS[note]
    return note


def to_flat_note(note: str) -> str:
    """Get note by replacing it by its corresponding flat note."""
    if note in SHARPY_ALTERATIONS:
        note = SHARPY_ALTERATIONS[note]
    return note


def scale_to_sharp(scale: List[str]) -> List[str]:
    """Get scale replacing each note by its sharp correspondant note."""
    flat_scale = list(scale)
    for i, note in enumerate(scale):
        sharp_note = to_sharp_note(note)
        flat_scale[i] = sharp_note
    return flat_scale


def scale_to_flat(scale: List[str]) -> List[str]:
    """Get scale replacing each note by its flat correspondant note."""
    flat_scale = list(scale)
    for i, note in enumerate(scale):
        sharp_note = to_flat_note(note)
        flat_scale[i] = sharp_note
    return flat_scale


def note_to_interval(note: str, root: str) -> int:
    """Get note from interval (int)."""
    sharp_note = to_sharp_note(note)
    idx = chromatic_position_from_root(sharp_note, root)
    return idx


def note_to_interval_name(note: str, root: str) -> str:
    """Get note from interval name."""
    idx = note_to_interval(note, root)
    return CHROMATICS_INTERVALS[idx]


def scale_to_intervals(scale: List[str], root: str) -> List[int]:
    """Get intervals from root.

    >>> scale_to_intervals(scale=['C','E','G'],root='C')
    [1,3,5]
    """
    intervals = []
    for note in scale:
        intervals.append(note_to_interval(note, root))
    return intervals


def scale_to_enharmonic(scale: List[str]) -> List[str]:
    """Modify the scale in order to not repeat note.

    Turns into enharmonic way if possible.

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
