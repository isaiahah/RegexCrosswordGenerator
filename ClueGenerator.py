from CrosswordGrid import CrosswordGrid, word_to_contents
from PremadePhrases import get_premade_phrases
from GroupManager import Group, GroupManager
from random import choice, sample, randint, shuffle
from string import ascii_uppercase, digits
from typing import Tuple, List

from SolutionGrid import SolutionGrid


def rand_letter(exclude: List[str] = None) -> str:
    """
    :param exclude: chars to not select
    :return: a random uppercase ASCII letter, not in exclude
    """
    if exclude is None:
        exclude = []
    letter = choice(ascii_uppercase)
    while letter in exclude:
        letter = choice(ascii_uppercase)
    return letter


def rand_number(exclude: List[str] = None) -> str:
    """
    :param exclude: chars to not select
    :return: a random ASCII digit, not in exclude
    """
    if exclude is None:
        exclude = []
    digit = choice(digits)
    while digit in exclude:
        digit = choice(digits)
    return digit

def rand_char(exclude: List[str] = None) -> str:
    """
    :param exclude: chars to not select
    :return: a random ASCII letter or digit, not in exclude
    """
    if exclude is None:
        exclude = []
    char = choice(ascii_uppercase + digits)
    while char in exclude:
        char = choice(ascii_uppercase + digits)
    return char

def rangechar(include: str) -> str:
    """
    :param include: character to match
    :return: one of \w, \W, \d, \D, or .
    """
    if include in ascii_uppercase:
        return choice(["\w", "\D", "."])
    if include in digits:
        return choice(["\W", "\d", "."])
    else:
        return "."


def make_range(include: List[str], exclude: List[str] = None) -> Tuple[str, List[str]]:
    """
    Generate a one-letter clue including all of the specified characters and not allowing any
    excluded characters.
    It generates 3 options, of which at most 2 will be from the premade phrases, then
    randomly selects one.

    Precondition: len(char) == 1 and char is uppercase

    :param include: characters to allow
    :param exclude: characters to not allow
    :return: clue and tuple of other solutions to the clue
    """
    if exclude is None:
        exclude = []

    # Consult bank of premade clues, select appropriate ones
    options = get_premade_phrases(include, exclude)

    # Want under 50-50 split of premade and novel clues
    if len(options) > 2:
        options = sample(options, 2)

    # Generate remaining clues by sampling random characters
    for _ in range(len(options), 3):
        new_clue = include.copy()
        for _ in range(randint(1, 5 - len(include))):
            new_clue.append(rand_char(exclude))
        new_clue = "".join(sorted(list(set(new_clue))))
        options.append("[" + new_clue + "]")

    chosen = choice(options)
    secondary = [symbol for symbol in chosen if symbol not in include]
    return chosen, secondary


def restrict_cell_two_ranges(char: str) -> Tuple[str, str]:
    """
    Create two one-letter clues which allow only the given character as a solution

    Precondition: len(char) == 1

    :param char: answer character desired
    :return: tuple of two clues
    """
    clue_1, exclude_1 = make_range([char])
    clue_2, exclude_2 = make_range([char], exclude_1)
    return clue_1, clue_2


def make_series_options(include: str) -> str:
    """
    Make a clue of two possible series. One is the given series and the other series
    has the same length but no shared characters.

    :param include: series to include
    :return: option of two series, both of same length with no shared characters.
    """
    other_series = ""
    for char in range(len(include)):
        other_series += rand_char(list(include))
    return "(" + include + "|" + other_series + ")"


class _ClueGenerator:
    _solution: str
    _rows: int
    _cols: int
    """
    Abstract class to generate clues. 
    
    _solution: Solution to the puzzle.
    _rows: rows in the Crossword grid
    _cols: columns in the Crossword grid
    """

    def __init__(self, solution: str, shape: Tuple[int, int]):
        """
        Create a ClueGenerator creating puzzles with the given solution and shape
        :param solution: solution to generated puzzles
        :param shape: shape of the crossword grid
        """
        self._solution = solution
        self._rows, self._cols = shape

    def generate_puzzle(self, filled: bool = False) -> CrosswordGrid:
        raise NotImplementedError()


class ClueGeneratorIndividualOptionPairs(_ClueGenerator):
    """
    Generate clues, specifying bracketed ranges for each letter.
    Each cell is individually specified by the two clues.
    """

    def generate_puzzle(self, filled: bool = False) -> CrosswordGrid:
        contents = word_to_contents(self._solution, (self._rows, self._cols))
        row_clues = ["" for _ in range(self._rows)]
        col_clues = ["" for _ in range(self._cols)]
        for row in range(self._rows):
            for col in range(self._cols):
                clues = list(restrict_cell_two_ranges(contents[row, col]))
                shuffle(clues)
                row_clues[row] += clues[0]
                col_clues[col] += clues[1]
        if not filled:
            contents = None
        return CrosswordGrid((self._rows, self._cols), contents=contents,
                             row_clues=row_clues, col_clues=col_clues)


class ClueGeneratorSeries(_ClueGenerator):
    """
    Generate clues, each of a bracketed option of letters and two
    strings of multiple letters.

    Precondition: Grid size must be at least 3 by 3
    """

    def generate_puzzle(self, filled: bool = False) -> CrosswordGrid:
        group_manager = GroupManager()
        solution_grid = SolutionGrid(self._solution, (self._rows, self._cols))
        curr_group = 0

        for row in range(self._rows):
            series_len = randint(2, 3)
            series_starts = randint(0, self._rows - series_len)
            series_indices = []
            series_word = ""
            for col in range(self._cols):
                if col in range(series_starts, series_starts + series_len):
                    series_indices.append((row, col))
                    series_word += solution_grid[(row, col)].get_char()
                else:
                    group_manager[curr_group] = Group("singleton", [(row, col)])
                    cell = solution_grid[(row, col)]
                    cell.add_group(curr_group)
                    specify_with = randint(0, 1)
                    if specify_with == 0:
                        row_clue, col_clue = restrict_cell_two_ranges(cell.get_char())
                        cell.set_row_clue(row_clue)
                        cell.set_col_clue(col_clue)
                    else:
                        specify_on = randint(0, 1)
                        if specify_on == 0:
                            cell.set_row_clue(cell.get_char())
                            cell.set_col_clue(".")
                        else:
                            cell.set_col_clue(cell.get_char())
                            cell.set_row_clue(".")
                    cell.set_defining_row_clue()
                    cell.set_defining_col_clue()
                    group_manager[curr_group].set_specified()
                    curr_group += 1
            group_manager[curr_group] = Group("series", series_indices)
            solution_grid.group_cells(series_indices, curr_group)
            solution_grid[series_indices[0]].set_defining_row_clue()
            solution_grid.set_row_clues(series_indices, make_series_options(series_word))
            curr_group += 1

        for col in range(self._cols):
            for row in range(self._rows):
                cell = solution_grid[(row, col)]
                if cell.get_col_clue() == "":
                    if not group_manager.get_group((row, col)).is_specified():
                        col_clue, _ = make_range([cell.get_char()])
                        cell.set_col_clue(col_clue)
                        cell.set_defining_col_clue()
                        group_manager.get_group((row, col)).set_specified()
                    else:
                        cell.set_col_clue(".")
                        cell.set_defining_col_clue()

        return solution_grid.to_crosswordgrid()


