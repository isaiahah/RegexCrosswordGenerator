from typing import List

phrase_list = []
with open("RegexEntities/PremadeClues.txt") as phrases_file:
    for phrase in phrases_file:
        phrase_list.append("[" + phrase.strip(" \n") + "]")


def get_premade_phrases(include: List[str], exclude: List[str]) -> List[str]:
    """
    Find the premade phrases containing all letters in includes and none of the
    letters in excludes

    Precondition: len(includes) > 0

    :param include: letters phrases must include
    :param exclude: letters phrases must exclude
    :return:
    """
    phrases = []
    for phrase in phrase_list:
        if (all([char in phrase for char in include]) and
                all([char not in phrase for char in exclude])):
            phrases.append(phrase)
    return phrases
