from flask import Request
from RegexEntities.PuzzleManager import PuzzleManager


class FlaskPuzzleManager(PuzzleManager):
    """
    Interface adapter for Flask page.

    Extends PuzzleManager, which contains use case methods
    """
    def update(self, update_data: Request) -> None:
        """
        Update the puzzle entries based on the given request
        :param update_data: Web request from the form, detailing the puzzle entries
        """
        for row in range(5):
            for col in range(5):
                self._puzzle[(row, col)] = \
                    get_request_item(update_data, str(row) + str(col)).upper()


def get_request_item(request: Request, item: str) -> str:
    """
    :param request: Request from the webpage form
    :param item: item in the form
    :return: value of item in given request
    """
    if request.method == 'POST':
        to_return = request.form[item]
    elif request.method == 'GET':
        to_return = request.args.get(item)
    else:
        raise Exception
    if to_return == '':
        to_return = ' '
    return to_return
