from typing import Any, List, Optional, Tuple

from fretboardgtr.constants import STANDARD_TUNING
from fretboardgtr.fretboards.config import FretBoardConfig


class HorizontalFretBoard:
    """Class containing the different elements of a fretboard.

    Also contains associated method to add some.
    """

    def __init__(
        self,
        tuning: Optional[List[str]] = None,
        config: Optional[FretBoardConfig] = None,
    ):
        self.tuning = tuning if tuning is not None else STANDARD_TUNING
        self.config = config if config is not None else FretBoardConfig()

    def get_list_in_good_order(self, _list: List[Any]) -> List[Any]:
        return _list[::-1]

    def get_background_start_position(self) -> Tuple[float, float]:
        open_fret_width = self.config.general.fret_width
        return (
            self.config.general.x_start + open_fret_width,
            self.config.general.y_start,
        )

    def get_background_dimensions(self) -> Tuple[float, float]:
        # We add 1 as it is one-indexed for first fret
        number_of_frets = (
            self.config.general.last_fret - self.config.general.first_fret
        ) + 1
        width = (number_of_frets) * (self.config.general.fret_width)
        height = (len(self.tuning) - 1) * self.config.general.fret_height
        return width, height

    def get_neck_dot_position(self, dot: int) -> List[Tuple[float, float]]:
        x = (
            self.config.general.x_start
            + (0.5 + dot - self.config.general.first_fret + 1)
            * self.config.general.fret_width
        )
        y = (
            self.config.general.y_start
            + (len(self.tuning) / 2 - (1 / 2)) * self.config.general.fret_height
        )
        if dot % 12 == 0:
            # Add two dots dot is multiple of 12
            lower_position = (
                x,
                y - self.config.general.fret_height,
            )
            upper_position = (
                x,
                y + self.config.general.fret_height,
            )
            return [lower_position, upper_position]
        else:
            center_position = (
                x,
                y,
            )
            return [center_position]

    def get_fret_position(
        self, fret_no: int
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        x = self.config.general.x_start + (self.config.general.fret_width) * (fret_no)
        y_start = self.config.general.y_start
        y_end = self.config.general.y_start + (self.config.general.fret_height) * (
            len(self.tuning) - 1
        )
        return (x, y_start), (x, y_end)

    def get_strings_position(
        self, string_no: int
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        open_fret_width = self.config.general.fret_width

        x_start = self.config.general.x_start + open_fret_width
        x_end = self.config.general.x_start + (
            self.config.general.fret_width
            + (self.config.general.last_fret - self.config.general.first_fret + 1)
            * self.config.general.fret_width
        )
        start = (
            x_start,
            self.config.general.y_start
            + (self.config.general.fret_height) * (string_no),
        )
        end = (
            x_end,
            self.config.general.y_start
            + (self.config.general.fret_height) * (string_no),
        )
        return start, end

    def get_nut_position(
        self,
    ) -> Optional[Tuple[Tuple[float, float], Tuple[float, float]]]:
        if self.config.general.first_fret != 1 or not self.config.general.show_nut:
            return None
        open_fret_width = self.config.general.fret_width

        start = (
            self.config.general.x_start + open_fret_width,
            self.config.general.y_start,
        )
        end = (
            self.config.general.x_start + open_fret_width,
            self.config.general.y_start
            + self.config.general.fret_height * (len(self.tuning) - 1),
        )
        return start, end

    def get_fret_number_position(self, dot: int) -> Tuple[float, float]:
        x = self.config.general.x_start + self.config.general.fret_width * (
            1 / 2 + dot - self.config.general.first_fret + 1
        )
        y = self.config.general.y_start + self.config.general.fret_height * (
            len(self.tuning)
        )
        return x, y

    def get_tuning_position(self, string_no: int) -> Tuple[float, float]:
        x = self.config.general.x_start + (
            self.config.general.fret_width
            * (self.config.general.last_fret - self.config.general.first_fret + 5 / 2)
        )
        y = self.config.general.y_start + self.config.general.fret_height * (string_no)
        return x, y

    def get_single_note_position(
        self, string_no: int, index: int
    ) -> Tuple[float, float]:
        x_pos = index + (1 / 2)
        x = self.config.general.x_start + (self.config.general.fret_width) * x_pos
        y = self.config.general.y_start + self.config.general.fret_height * (string_no)
        return x, y

    def get_cross_position(self, string_no: int) -> Tuple[float, float]:
        x = self.config.general.x_start + self.config.general.fret_width * (1 / 2)
        y = self.config.general.y_start + (self.config.general.fret_height) * (
            string_no
        )
        return x, y

    def get_size(self) -> Tuple[float, float]:
        """Get total size of the drawing.

        Returns
        -------
        Tuple[float, float]
            Width and heigth
        """
        # We add 1 as it is one-indexed for first fret
        number_of_frets = (
            self.config.general.last_fret - self.config.general.first_fret
        ) + 1
        width = (
            self.config.general.x_start
            + self.config.general.fret_width * (number_of_frets + 2)
            + self.config.general.x_end_offset
        )
        height = (
            self.config.general.y_start
            + self.config.general.fret_height * (len(self.tuning) + 1)
            + self.config.general.y_end_offset
        )
        return (width, height)

    def get_inside_bounds(
        self,
    ) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        """Get the size of the inner drawing.

        This function could be use to add custom elements

        Returns
        -------
        Tuple[Tuple[float, float], Tuple[float, float]]
            Upper left corner x coordinate, upper left corner y coordinate
            Lower right corner x coordinate, lower right corner y coordinate
        """
        open_fret_width = self.config.general.fret_width
        # We add 1 as it is one-indexed for first fret
        number_of_frets = (
            self.config.general.last_fret - self.config.general.first_fret
        ) + 1
        upper_left_x = self.config.general.x_start
        upper_left_y = self.config.general.y_start
        lower_right_x = (
            self.config.general.x_start
            + open_fret_width
            + (number_of_frets) * (self.config.general.fret_width)
        )
        lower_right_y = (
            self.config.general.y_start
            + (len(self.tuning) - 1) * self.config.general.fret_height
        )
        return ((upper_left_x, upper_left_y), (lower_right_x, lower_right_y))
