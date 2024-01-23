from typing import Collection, Dict, List, Tuple

from fretboardgtr.constants import (
    CHROMATICS_INTERVALS,
    CHROMATICS_NOTES,
    DOTS_POSITIONS,
    FLAT_ALTERATIONS,
    SHARP_ALTERATIONS,
)
from fretboardgtr.notes import Note


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


def _enharmonic_duplicates(scale: List[str]) -> Dict[str, List[Tuple[str, int]]]:
    base_notes_scale = [note[0] for note in scale]
    duplicates: Dict[str, List[Tuple[str, int]]] = {}
    for idx, (real_note, base_note) in enumerate(zip(scale, base_notes_scale)):
        if base_note in duplicates:
            duplicates[base_note].append((real_note, idx))
        else:
            duplicates[base_note] = [(real_note, idx)]

    # Remove key if there is only one note
    duplicates = {key: value for key, value in duplicates.items() if len(value) > 1}
    return duplicates


def _tuple_note_custom_sort(item: Tuple[str, int]) -> Tuple[str, int]:
    """Sort b prefix first, then no prefix, then # prefix."""
    note = item[0]
    letter = note[0]
    modifier = note[1:]

    if modifier == "b":
        return (letter, 0)
    elif modifier == "#":
        return (letter, 2)
    else:
        return (letter, 1)


def __scale_to_enharmonic_sharp(
    duplicates: Dict[str, List[Tuple[str, int]]], _scale: List[Note]
) -> List[Note]:
    # We choose to take '#'-suffix duplicated first to flatten
    # If not availale take without prefix
    # Let's say we have these duplicates
    # ["G", "G#"] Then take G#
    # ["Gb", "G", "G#"] Then take G#
    # ["Gb", "G"] Then take G
    # Once taken use the flat_enharmonic function to get the flat equivalent
    # Of the given note
    for _, notes in duplicates.items():
        sorted_notes = sorted(notes, key=_tuple_note_custom_sort)
        _, idx = sorted_notes[-1]
        _scale[idx] = _scale[idx].flat_enharmonic()
        break
    return _scale


def __scale_to_enharmonic_flat(
    duplicates: Dict[str, List[Tuple[str, int]]], _scale: List[Note]
) -> List[Note]:
    # We choose to take 'b'-suffix duplicated first to flatten
    # If not availale take without prefix
    # Let's say we have these duplicates
    # ["G", "G#"] Then take G
    # ["Gb", "G", "G#"] Then take Gb
    # ["Gb", "G"] Then take Gb
    # Once taken use the sharp_enharmonic function to get the sharp equivalent
    # Of the given note
    for _, notes in duplicates.items():
        sorted_notes = sorted(notes, key=_tuple_note_custom_sort)
        _, idx = sorted_notes[0]
        _scale[idx] = _scale[idx].sharp_enharmonic()
        break
    return _scale


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
    # Not possible to get enharmonic scale if there is more than 7 notes
    if len(scale) > 7:
        return scale
    # 7 times the max scale seems pretty good as we cover all the possible alterations
    MAX_RETRY = 7 * 7

    # Attempt to convert duplicate notes in the scale to their sharp enharmonic
    # equivalents until there are no more duplicates or the maximum number of
    # retries is reached.
    # It is kind of recursive, so we can get C####### in some case for example
    sharp_duplicates = _enharmonic_duplicates(scale)
    sharp_tries = 0
    sharp_scale: List[Note] = [Note(note) for note in scale]
    while sharp_duplicates:
        sharp_scale = __scale_to_enharmonic_sharp(sharp_duplicates, sharp_scale)
        sharp_duplicates = _enharmonic_duplicates([note.name for note in sharp_scale])
        sharp_tries += 1
        if sharp_tries > MAX_RETRY:
            break

    # Attempt to convert duplicate notes in the scale to their flat enharmonic
    # equivalents until there are no more duplicates or the maximum number
    # of retries is reached.
    # It is kind of recursive, so we can get Cbbbbbbb in some case for example
    flat_duplicates = _enharmonic_duplicates(scale)
    flat_scale: List[Note] = [Note(note) for note in scale]
    flat_tries = 0
    while flat_duplicates:
        flat_scale = __scale_to_enharmonic_flat(flat_duplicates, flat_scale)
        flat_duplicates = _enharmonic_duplicates([note.name for note in flat_scale])
        flat_tries += 1
        if flat_tries > MAX_RETRY:
            break

    # After attempting enharmonic conversions, determine the optimal scale to use.
    # If both sharp and flat scales have no duplicates, we compare them based on the
    # total number of alterations (sharps or flats) and select the one with fewer
    # alterations.
    # In case of a tie, we avoid scales with unusual alterations like E# or Cb.
    if len(sharp_duplicates) == 0 and len(flat_duplicates) == 0:
        # Count total number of alteration
        sharp_alterations = sum([len(note.name[1:]) for note in sharp_scale])
        flat_alterations = sum([len(note.name[1:]) for note in flat_scale])
        # Choose scale with fewer alterations
        if sharp_alterations == flat_alterations:
            sharp_weird_alteration = "E#" in sharp_scale or "B#" in sharp_scale
            flat_weird_alteration = "Cb" in flat_scale or "Fb" in flat_scale
            if sharp_weird_alteration:
                return [note.name for note in flat_scale]
            if flat_weird_alteration:
                return [note.name for note in sharp_scale]

        elif sharp_alterations < flat_alterations:
            return [note.name for note in sharp_scale]
        else:
            return [note.name for note in flat_scale]
    # If only one of the scales (sharp or flat) has no duplicates, return that scale.
    if not sharp_duplicates:
        return [note.name for note in sharp_scale]
    if not flat_duplicates:
        return [note.name for note in flat_scale]
    return scale
