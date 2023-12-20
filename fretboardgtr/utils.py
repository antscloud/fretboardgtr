from typing import Collection, List, Tuple

from fretboardgtr.constants import (
    CHROMATICS_INTERVALS,
    CHROMATICS_NOTES,
    DOTS_POSITIONS,
    ENHARMONICS,
    FLAT_ALTERATIONS,
    SHARP_ALTERATIONS,
)


def get_valid_dots(first_fret: int, last_fret: int) -> List[int]:
    """Get the valid fretboard dots between frets.

    Parameters
    ----------
    first_fret : int
        First fret
    last_fret : int
        Last fret

    Returns
    -------
    List[int]
        Valid dots between frets
    """
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


def to_sharp_note(note: str) -> str:
    """Get note by replacing it by its corresponding sharp note."""
    if note in FLAT_ALTERATIONS:
        note = FLAT_ALTERATIONS[note]
    return note


def to_flat_note(note: str) -> str:
    """Get note by replacing it by its corresponding flat note."""
    if note in SHARP_ALTERATIONS:
        note = SHARP_ALTERATIONS[note]
    return note


def chromatic_position_from_root(note: str, root: str) -> int:
    """Get the index of the note from the root on chromatic scale."""
    idx = 0
    chroma_from_root = chromatics_from_root(root)
    for _idx, chromatic_note in enumerate(chroma_from_root):
        if chromatic_note == to_sharp_note(note):
            idx = _idx
    return idx


def scale_to_sharp(scale: List[str]) -> List[str]:
    """Get scale replacing each note by its sharp correspondant note."""
    sharp_scale = list(scale)
    for i, note in enumerate(scale):
        sharp_note = to_sharp_note(note)
        sharp_scale[i] = sharp_note
    return sharp_scale


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


def resolve_high_alterations_in_scale(scale: List[str]) -> List[str]:
    """Resolve multiple flat or sharp in scale."""
    for i, note in enumerate(scale):
        if len(note) <= 2:
            continue
        base_note, high_alterations = note[0:1], note[2:]
        new_note = base_note
        if "b" in high_alterations:
            new_note = CHROMATICS_NOTES[
                (CHROMATICS_NOTES.index(base_note) - (len(high_alterations) + 1)) % 12
            ]
        elif "#" in high_alterations:
            new_note = CHROMATICS_NOTES[
                (CHROMATICS_NOTES.index(base_note) + (len(high_alterations) + 1)) % 12
            ]
        scale[i] = new_note

    return scale


def sort_scale(scale: List[str]) -> List[str]:
    def _sort_scale(item: str) -> Tuple[str, int]:
        letter = item[0]
        modifier = item[1:]

        if modifier == "b":
            return (letter, 0)
        elif modifier == "#":
            return (letter, 2)
        else:
            return (letter, 1)

    return sorted(scale, key=_sort_scale)


def _scale_to_enharmonic(scale: List[str]) -> List[str]:
    # Resolve high alterations
    scale = resolve_high_alterations_in_scale(scale)
    # Remove duplicates
    scale = list(set(scale))
    # Sort scale
    scale = sort_scale(scale)
    # Try to make all flat notes unique
    flat_scale = scale_to_flat(scale)
    unique_flat_scale = set(note.split("b")[0] for note in flat_scale)
    if len(unique_flat_scale) == len(flat_scale):
        return flat_scale
    # Try to replace E with Fb if there is still duplicates
    if "E" in flat_scale:
        flat_scale = [ENHARMONICS["E"] if note == "E" else note for note in flat_scale]
        unique_flat_scale = set(note.split("b")[0] for note in flat_scale)
        if len(unique_flat_scale) == len(flat_scale):
            return flat_scale
    # Try to replace B with Cb if there is still duplicates
    if "B" in flat_scale:
        flat_scale = [ENHARMONICS["B"] if note == "B" else note for note in flat_scale]
        unique_flat_scale = set(note.split("b")[0] for note in flat_scale)
        if len(unique_flat_scale) == len(flat_scale):
            return flat_scale

    # Try to make all sharp notes unique
    sharp_scale = scale_to_sharp(scale)
    unique_sharp_notes = set(note.split("#")[0] for note in sharp_scale)
    if len(unique_sharp_notes) == len(sharp_scale):
        return sharp_scale

    # Try to replace F with E# if there is still duplicates
    if "F" in sharp_scale:
        sharp_scale = [
            ENHARMONICS["F"] if note == "F" else note for note in sharp_scale
        ]
        unique_sharp_notes = set(note.split("#")[0] for note in sharp_scale)
        if len(unique_sharp_notes) == len(sharp_scale):
            return sharp_scale

    # Try to replace C with B# if there is still duplicates
    if "C" in sharp_scale:
        sharp_scale = [
            ENHARMONICS["C"] if note == "C" else note for note in sharp_scale
        ]
        unique_sharp_notes = set(note.split("#")[0] for note in sharp_scale)
        if len(unique_sharp_notes) == len(sharp_scale):
            return sharp_scale
    return scale


def scale_to_enharmonic(scale: List[str]) -> List[str]:
    """Modify the scale in order to not repeat note.

    Turns into enharmonic way if possible. Otherwise return the original scale.

    >>> scale_to_enharmonic(['A#', 'C', 'D', 'D#', 'F', 'G', 'A'])
        ['Bb', 'C', 'D', 'Eb', 'F', 'G', 'A']
    >>> scale_to_enharmonic(["A","A#","B","C","C#","D","D#","E","F","F#","G","G#"])
        ['A', 'A#', 'B', 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#']
    >>> scale_to_enharmonic(['F#', 'G#', 'A#', 'B', 'C#', 'D#', 'F'])
        ['Gb', 'Ab', 'Bb', 'Cb', 'Db', 'Eb', 'F']
    """
    return sort_scale(_scale_to_enharmonic(scale))
