from typing import List, Tuple, Dict


class Group:
    _indices: List[Tuple[int, int]]
    _type: str
    _specified: bool
    """
    _indices: Indices in the group
    _type: type of group, reflects reason for grouping
    _specified: if the group is uniquely specified
    """

    def __init__(self, type: str, indices: List[Tuple[int, int]]):
        self._indices = indices
        self._type = type
        self._specified = False

    def get_indices(self) -> List[Tuple[int, int]]:
        return self._indices

    def get_type(self) -> str:
        return self._type

    def is_specified(self) -> bool:
        return self._specified

    def set_specified(self, value: bool = True) -> None:
        self._specified = value


class GroupManager:
    _groups: Dict[int, Group]
    """
    _groups: key is group number, value is Group
    """

    def __init__(self):
        self._groups = {}

    def __setitem__(self, group_number: int, group: Group) -> None:
        self._groups[group_number] = group

    def __getitem__(self, group_number: int) -> Group:
        return self._groups[group_number]

    def get_group(self, index: Tuple[int, int]) -> Group:
        for group in self._groups.values():
            if index in group.get_indices():
                return group
