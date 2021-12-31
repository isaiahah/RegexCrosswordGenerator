from typing import Dict, Tuple, List
from RegexEntities.CrosswordGrid import CrosswordGrid, word_to_contents


class SolutionCell:
    _char: str
    _groups: List[int]
    _row_clue: str
    _defining_row_clue: bool
    _col_clue: str
    _defining_col_clue: bool
    """
    _char: character in the cell
    _groups: group numbers of the cell. If one cell in a group is uniquely
    identified, they all are
    _row_clue: the row clue appropriate to this cell. It may also define other cells
    _defining_row_clue: if the row clue is first used in the cell
    _col_clue: the column clue appropriate to this cell. It may also define other cells
    _defining_col_clue: if the column clue is first used in the cell
    """

    def __init__(self, char: str):
        """
        Create a new Cell with the given character
        :param char: character in the cell
        """
        self._char = char
        self._groups = []
        self._row_clue = ""
        self._defining_row_clue = False
        self._col_clue = ""
        self._defining_col_clue = False

    def get_char(self) -> str:
        """
        :return: char stored in this cell
        """
        return self._char

    def add_group(self, group: int) -> None:
        """
        Set the group of this cell
        """
        self._groups.append(group)

    def get_groups(self) -> List[int]:
        """
        :return: the groups for this cell
        """
        return self._groups

    def get_col_clue(self) -> str:
        """
        :return: the column clue for this cell
        """
        return self._col_clue

    def set_col_clue(self, col_clue: str) -> None:
        """
        Set the column clue of this cell
        """
        self._col_clue = col_clue

    def is_defining_col_clue(self) -> bool:
        """
        :return: whether this cell's column clue defines the group
        """
        return self._defining_col_clue

    def set_defining_col_clue(self, value: bool = True) -> None:
        """
        Set whether the column clue defines the group
        :param value: if the column clue defines the group
        """
        self._defining_col_clue = value

    def get_row_clue(self) -> str:
        """
        :return: the row clue for this cell
        """
        return self._row_clue

    def set_row_clue(self, row_clue: str) -> None:
        """
        Set the row clue of this cell
        """
        self._row_clue = row_clue

    def is_defining_row_clue(self) -> bool:
        """
        :return: whether this cell's row clue defines the capture group
        """
        return self._defining_row_clue

    def set_defining_row_clue(self, value: bool = True) -> None:
        """
        Set whether the row clue defines the group
        :param value: if the row clue defines the group
        """
        self._defining_row_clue = value


class SolutionGrid:
    _rows: int
    _cols: int
    _contents: Dict[Tuple[int, int], SolutionCell]
    """
    _rows: number of rows in the crossword grid
    _cols: number of columns in the crossword grid
    _contents: Dict with keys (row, col) and value of the SolutionCells at that position
    """

    def __init__(self, solution: str, shape: Tuple[int, int]):
        """
        Create a new SolutionGrid with the given solution and shape.

        Precondition: len(solution) == shape[0] * shape[1]

        :param solution: the solution to the crossword
        :param shape: the shape of the crossword grid
        """
        self._rows, self._cols = shape
        self._contents = {}
        for row in range(self._rows):
            for col in range(self._cols):
                self._contents[(row, col)] = \
                    SolutionCell(solution[row * self._cols + col])

    def __getitem__(self, index: Tuple[int, int]) -> SolutionCell:
        """
        Return the SolutionCell at the given index

        Precondition: 0 <= index[0] <= self._rows and 0 <= index[1] <= self._cols

        :param index: row and column to examine
        :return: SolutionCell at the given index
        """
        return self._contents[index]

    def get_row_clues(self) -> List[str]:
        """
        Combine the row clues for each cell into a full row clue
        :return: list of row clues
        """
        row_clues_phrases = [[] for _ in range(self._rows)]
        row_clues = ["" for _ in range(self._rows)]
        for row in range(self._rows):
            for col in range(self._cols):
                cell = self._contents[(row, col)]
                if cell.is_defining_row_clue():
                    row_clues_phrases[row].append(cell.get_row_clue())
            row_clues[row] = combine_to_clue(row_clues_phrases[row])
        return row_clues

    def get_col_clues(self) -> List[str]:
        """
        Combine the column clues for each cell into a full column clue
        :return: list of column clues
        """
        col_clues_phrases = [[] for _ in range(self._cols)]
        col_clues = ["" for _ in range(self._cols)]
        for col in range(self._cols):
            for row in range(self._rows):
                cell = self._contents[(row, col)]
                if cell.is_defining_col_clue():
                    col_clues_phrases[col].append(cell.get_col_clue())
            col_clues[col] = combine_to_clue(col_clues_phrases[col])
        return col_clues

    def group_cells(self, indices: List[Tuple[int, int]], group: int) -> None:
        """
        Group several cells together, assigning them to the given group

        Precondition: all indexes are valid

        :param indices: indices of cells to group
        :param group: group number to assign
        """
        for index in indices:
            self._contents[index].add_group(group)

    def set_row_clues(self, indices: List[Tuple[int, int]], row_clue: str) -> None:
        """
        Set the row clue for several cells.

        Precondition: all indexes are valid

        :param indices: indices of cells to set row clue
        :param row_clue: row clue to set
        """
        for index in indices:
            self._contents[index].set_row_clue(row_clue)

    def set_col_clues(self, indices: List[Tuple[int, int]], col_clue: str) -> None:
        """
        Set the column clue for several cells.

        Precondition: all indexes are valid

        :param indices: indices of cells to set column clue
        :param col_clue: column clue to set
        """
        for index in indices:
            self._contents[index].set_col_clue(col_clue)

    def get_solution(self) -> str:
        """
        :return: the solution stored in the grid
        """
        solution = ""
        for row in range(self._rows):
            for col in range(self._cols):
                solution += self._contents[(row, col)].get_char()
        return solution

    def to_crosswordgrid(self) -> CrosswordGrid:
        """
        Create a CrosswordGrid based on this grid
        :return: CrosswordGrid with identical contents and clues
        """
        shape = (self._rows, self._cols)
        contents = word_to_contents(self.get_solution(), shape)
        row_clues = self.get_row_clues()
        col_clues = self.get_col_clues()
        return CrosswordGrid(shape, contents=contents,
                             row_clues=row_clues, col_clues=col_clues)


def combine_to_clue(parts: List[str]) -> str:
    """
    Combine the given regular expression pieces into one regular expression.

    Precondition: len(parts) > 0

    :param parts: parts of the regular expression
    :return: single regular expression containing all parts
    """
    combined = parts[0]
    prev = parts[0]
    done_last = "append"
    for i in range(1, len(parts)):
        curr = parts[i]
        if curr != prev:
            combined += curr
            done_last = "append"
        else:
            if done_last == "append":
                combined += "+"
                done_last = "add +"
            if done_last == "add +":
                pass
        prev = curr
    return combined
