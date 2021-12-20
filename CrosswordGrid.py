from typing import List, Tuple
import re
from numpy import ndarray, array


class CrosswordGrid:
    _rows: int
    _cols: int
    _contents: ndarray  # ndarray used to enforce shape and string lengths
    _row_clues: List[str]
    _col_clues: List[str]
    """
    _rows: number of rows in the crossword grid
    _cols: number of columns in the crossword grid
    _contents: contents of the crossword
    _row_clues: clues on the crossword rows
    _col_clues: clues on the crossword columns
    """

    def __init__(self, shape: Tuple[int, int], contents: ndarray = None,
                 row_clues: List[str] = None, col_clues: List[str] = None):
        """
        Construct a new Crossword grid. The number of rows and columns must
        be specified, the contents and clues are optional and will be left
        blank otherwise.

        Precondition: if provided, the contents and clues are of appropriate sizes

        :param shape: shape of the crossword grid
        :param contents: optional, contents of filled cells. Empty if not specified.
        :param row_clues: optional, clues for the rows. Empty if not specified.
        :param col_clues: optional, clues for the columns. Empty if not specified.
        """
        self._rows, self._cols = shape

        if contents is None:
            contents = array([[' ' for _ in range(self._cols)]
                              for _ in range(self._rows)],
                             dtype='U1')
        self._contents = contents

        if row_clues is None:
            row_clues = ['' for _ in range(self._rows)]
        self._row_clues = row_clues

        if col_clues is None:
            col_clues = ['' for _ in range(self._cols)]
        self._col_clues = col_clues

    def __getitem__(self, index: Tuple[int, int]) -> str:
        """
        Given Tuple (i, j), return the letter in row i column j of the crossword.

        Precondition: 0 <= i <= self._rows and 0 <= j <= self._cols

        :param index: crossword position to examine
        :return: the character at the given position
        """
        return self._contents[index]

    def __setitem__(self, index: Tuple[int, int], value: str) -> None:
        """
        Given Tuple (i, j), set the letter in row i column j of the crossword.
        Only the first character will be set

        Precondition: 0 <= i <= self._rows and 0 <= j <= self._cols

        :param index: crossword position to set
        :param value: value to set position to
        """
        self._contents[index] = value

    def clear(self) -> None:
        """
        Blank the crossword contents.
        """
        for row in range(self._rows):
            for col in range(self._cols):
                self._contents[row, col] = " "

    def __str__(self) -> str:
        """
        :return: String representation of the crossword grid
        """
        col_width = [len(col_clue) + 2 for col_clue in self._col_clues]
        col_width.insert(0, max([len(row_clue) + 2 for row_clue in self._row_clues]))
        table_length = sum(col_width) + len(col_width) + 1

        output = ("-" * table_length) + "\n"
        output += "|{0:^{row_clue_len}}|".format("", row_clue_len=col_width[0])
        for col in range(self._cols):
            output += "{0:^{col_len}}|".format(self._col_clues[col],
                                               col_len=col_width[col + 1])
        output += "\n"
        output += ("-" * table_length) + "\n"

        for row in range(self._rows):
            output += "|{0:^{row_clue_len}}|".format(self._row_clues[row],
                                                     row_clue_len=col_width[0])
            for col in range(self._cols):
                output += "{0:^{col_len}}|".format(self._contents[row, col],
                                                   col_len=col_width[col + 1])
            output += "\n"
            output += ("-" * table_length) + "\n"
        return output

    def set_row_clues(self, row_clues: List[str]) -> None:
        """
        Set the row clues to the given values

        Precondition: len(row_clues) == self._rows

        :param row_clues: values to set the row clues to
        """
        self._row_clues = row_clues

    def set_col_clues(self, col_clues: List[str]) -> None:
        """
        Set the column clues to the given values

        Precondition: len(col_clues) == self._cols

        :param col_clues: values to set the column clues to
        """
        self._col_clues = col_clues

    def get_row(self, index: int) -> str:
        """
        Precondition: 0 <= index <= self._rows

        :param index: index of crossword row
        :return: the word formed by the given row
        """
        word = ""
        for col in range(self._cols):
            word += self._contents[index, col]
        return word

    def get_col(self, index: int) -> str:
        """
        Precondition: 0 <= index <= self._cols

        :param index: index of crossword column
        :return: the word formed by the given column
        """
        word = ""
        for row in range(self._rows):
            word += self._contents[row, index]
        return word

    def row_check(self) -> bool:
        """
        Check the rows of the crossword
        :return: True if the words in the rows match the row clues
        """
        for row in range(self._rows):
            if re.search("^" + self._row_clues[row] + "$", self.get_row(row)) is None:
                return False
        return True

    def col_check(self) -> bool:
        """
        Check the columns of the crossword
        :return: True if the words in the columns match the column clues
        """
        for col in range(self._cols):
            if re.search("^" + self._col_clues[col] + "$", self.get_col(col)) is None:
                return False
        return True

    def grid_check(self) -> bool:
        """
        Check the full crossword grid
        :return: True if the grid state matches both row and column clues
        """
        return self.row_check() and self.col_check()


def word_to_contents(word: str, shape: Tuple[int, int]) -> ndarray:
    """
    Shape a word into an ndarray which can be used as crossword contents

    Precondition: len(word) == shape[0] * shape[1]

    :param word: the word to reshape
    :param shape: the ndarray shape
    :return: ndarray of given shape with word along rows
    """
    contents = ndarray(shape=shape, dtype="U1")
    curr_row = 0
    curr_col = 0
    for char in word:
        contents[curr_row, curr_col] = char
        curr_col += 1
        if curr_col == shape[1]:
            curr_row += 1
            curr_col = 0
    return contents

