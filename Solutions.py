from __future__ import annotations
from csv import reader
from random import sample, choices
from typing import List, Tuple
from string import ascii_uppercase, digits

solutions_list = []
with open("PremadeSolutions.csv", newline="") as solutions_file:
    solutions_reader = reader(solutions_file)
    for row in solutions_reader:
        solutions_list.append((row[0], row[1]))
solutions_list = solutions_list[1:]  # Remove header


class PremadeSolutionIterator:
    _solutions: List[Tuple[str, str]]
    _at: int
    """
    Class to iterate over premade solutions and hints
    
    _solutions: Premade Pairs of (Hint, Solution)
    _at: Index of next pair to return
    """
    def __init__(self):
        self._solutions = sample(solutions_list, len(solutions_list))

    def __iter__(self) -> PremadeSolutionIterator:
        self._at = 0
        return self

    def __next__(self) -> Tuple[str, str]:
        if self._at < len(solutions_list):
            to_return = self._solutions[self._at]
            self._at += 1
            return to_return
        else:
            raise StopIteration


class RandomSolutionIterator:
    """
    Class to infinitely generate solutions of 25 random characters
    """
    def __iter__(self):
        return self

    def __next__(self):
        solution = "".join(choices(list(ascii_uppercase) + list(digits), k=25))
        return ("No Hint", solution)
