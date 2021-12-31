from RegexEntities import ClueGenerator, CrosswordGrid, Solutions
from typing import List


class PuzzleManager:
    """
    Class to generate and check the puzzles.

    Essentially a use case, even though it is never directly instantiated.
    """
    _premade_solution: Solutions.PremadeSolutionIterator
    _num_premade: int
    _at_premade: int
    _random_solution: Solutions.RandomSolutionIterator
    _puzzle: CrosswordGrid.CrosswordGrid

    def __init__(self):
        self._premade_solutions = Solutions.PremadeSolutionIterator()
        self._num_premade = self._premade_solutions.len_premade()
        self._at_premade = 0
        self._random_solutions = Solutions.RandomSolutionIterator()
        self.new_premade_puzzle()

    def new_premade_puzzle(self) -> None:
        """
        Set self._puzzle to a new puzzle with premade solution.
        If no remaining premade clues are available, return a random puzzle.
        """
        try:
            hint, solution = next(self._premade_solutions)
            self._puzzle = generate_puzzle(solution, hint)
            self._at_premade += 1
        except StopIteration:
            self.new_random_puzzle()

    def new_random_puzzle(self) -> None:
        """
        Set self._puzzle to a new puzzle with random solution
        """
        hint, solution = next(self._random_solutions)
        self._puzzle = generate_puzzle(solution, hint)

    def get_puzzle(self) -> CrosswordGrid.CrosswordGrid:
        """
        :return: Current crossword puzzle
        """
        return self._puzzle

    def get_hint(self) -> str:
        """
        :return: Hint for current crossword puzzle
        """
        return self._puzzle.get_hint()

    def get_row_clues(self) -> List[str]:
        """
        :return: Row clues for current crossword puzzle
        """
        return self._puzzle.get_row_clues()

    def get_col_clues(self) -> List[str]:
        """
        :return: Column clues for current crossword puzzle
        """
        return self._puzzle.get_col_clues()

    def check_puzzle(self) -> bool:
        """
        :return: True if the current crossword puzzle is solved
        """
        return self._puzzle.grid_check()

    def premade_remain(self) -> bool:
        """
        :return: True if unused premade solutions remain
        """
        return self._at_premade < self._num_premade

    def update(self, update_data) -> None:
        """
        Update the puzzle entries based on input data
        """
        raise NotImplementedError


def generate_puzzle(solution: str, hint: str) -> CrosswordGrid.CrosswordGrid:
    """
    Construct a puzzle with the given solution and hint.
    Uses the ClueGeneratorSeries
    :param solution: solution to the puzzle
    :param hint: hint for the puzzle
    :return: puzzle with given hint and clues uniquely specifying given solution
    """
    clue_generator = ClueGenerator.ClueGeneratorSeries(solution, (5, 5))
    puzzle = clue_generator.generate_puzzle()
    puzzle.set_hint(hint)
    return puzzle
