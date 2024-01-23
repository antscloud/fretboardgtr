from typing import Tuple

from fretboardgtr.constants import FLAT_CHROMATICS_NOTES, SHARP_CHROMATICS_NOTES


class Note:
    _BASE_NOTES = ["A", "B", "C", "D", "E", "F", "G"]
    _BASE_NOTES_DISTANCE = [2, 2, 1, 2, 2, 1, 2]

    def __init__(self, name: str):
        self.name = name
        if not self.check_if_valid():
            raise ValueError(f"{name} is not a valid note")

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return self.name

    def base_note(self) -> str:
        return self.name[0]

    def _resolve(self, prefer_flat: bool = True) -> str:
        if len(self.name) == 1:
            return self.name

        chromatic_scale = (
            FLAT_CHROMATICS_NOTES if prefer_flat else SHARP_CHROMATICS_NOTES
        )
        if self.name in chromatic_scale:
            return self.name

        base_note, alterations = self.name[0:1], self.name[1:]
        new_note = base_note
        if "b" in alterations:
            new_note = chromatic_scale[
                (chromatic_scale.index(base_note) - (len(alterations))) % 12
            ]
        elif "#" in alterations:
            new_note = chromatic_scale[
                (chromatic_scale.index(base_note) + (len(alterations))) % 12
            ]

        return new_note

    def resolve(self, prefer_flat: bool = True) -> "Note":
        """Resolve alterations in notes."""
        return Note(self._resolve(prefer_flat))

    def check_if_valid(self) -> bool:
        resolved_note = self._resolve()
        return (
            resolved_note in SHARP_CHROMATICS_NOTES
            or resolved_note in FLAT_CHROMATICS_NOTES
        )

    def sharpen(self) -> "Note":
        """Sharpen the note name by increasing the pitch by one semitone.

        Returns
        -------
        Note
            The sharpened note
        """
        # If the note name has only one letter, just add a "#" at the end
        if len(self.name) == 1:
            return Note(self.name + "#")

        base_note, alterations = self.name[0:1], self.name[1:]

        # If the note has a flat alteration, remove it
        if "b" in alterations:
            return Note(base_note + alterations[:-1])

        if "#" in alterations:
            return Note(self.name + "#")

        return self

    def flatten(self) -> "Note":
        """Flatten the note name by decreasing the pitch by one semitone.

        Returns
        -------
        Note
            The flattened note
        """
        # If the note has only one character, just add 'b' to it
        if len(self.name) == 1:
            return Note(self.name + "b")

        base_note, alterations = self.name[0:1], self.name[1:]

        if "b" in alterations:
            return Note(self.name + "b")

        # If the note has '#' in its alterations, remove the sharp
        if "#" in alterations:
            return Note(base_note + alterations[:-1])

        return self

    def __next_base_note(self, base_note: str) -> Tuple[str, int]:
        idx_base_note = self._BASE_NOTES.index(base_note)
        next_idx = (idx_base_note + 1) % 7
        return self._BASE_NOTES[next_idx], self._BASE_NOTES_DISTANCE[next_idx]

    def __previous_base_note(self, base_note: str) -> Tuple[str, int]:
        idx_base_note = self._BASE_NOTES.index(base_note)
        next_idx = (idx_base_note - 1) % 7
        # We add 1 to the note distance because as we're going backward,
        # we need to use the n+1 interval
        return self._BASE_NOTES[next_idx], self._BASE_NOTES_DISTANCE[(next_idx + 1) % 7]

    def flat_enharmonic(self) -> "Note":
        """Transform the note into its enharmonic flat equivalent.

        If the note has alterations, it retains them and applies flats
        instead of sharps.

        Returns
        -------
        Note
            The enharmonic equivalent note with flats.
        """
        # Get the base note and any alterations
        base_note = self.name[0:1]
        alterations = self.name[1:] if len(self.name) >= 2 else None

        # Apply alterations
        if alterations is not None and "#" in alterations:
            return self.resolve(prefer_flat=True)

        target_note, distance = self.__next_base_note(base_note)

        if alterations is not None and "b" in alterations:
            return Note(target_note + alterations + "b" * distance)
        else:
            flats_to_add = "b" * distance
            return Note(target_note + flats_to_add)

    def sharp_enharmonic(self) -> "Note":
        """Transform the note into its enharmonic sharp equivalent.

        If the note has alterations, it retains them and applies sharps
        instead of flats.

        Returns
        -------
        Note
            The enharmonic equivalent note with sharps.
        """
        # Get the base note and any alterations
        base_note = self.name[0:1]
        alterations = self.name[1:] if len(self.name) >= 2 else None

        # Apply alterations
        if alterations is not None and "b" in alterations:
            return self.resolve(prefer_flat=False)

        target_note, distance = self.__previous_base_note(base_note)

        if alterations is not None and "#" in alterations:
            return Note(target_note + alterations + "#" * distance)
        else:
            sharps_to_add = "#" * distance
            return Note(target_note + sharps_to_add)
