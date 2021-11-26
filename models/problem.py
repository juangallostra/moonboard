from dataclasses import dataclass
from typing import List


@dataclass
class Setter:
    """
    Information about the setter of the problem.

    :param nickname: The setter's nickname
    :type nickname: str
    :param firstname: The setter's first name
    :type firstname: str
    :param lastname: The setter's last name
    :type lastname: str
    """
    nickname: str
    firstname: str
    lastname: str


@dataclass
class Move:
    """
    Information about a move of the problem.

    :param id: The move's id
    :type id: int
    :param description: The move's description
    :type description: str
    :param is_start: Whether the move is the start of the problem
    :type is_start: bool
    :param is_end: Whether the move is the end of the problem
    :type is_end: bool
    """
    id: int
    row: int
    column: int
    description: str
    is_start: bool = False
    is_end: bool = False


class Problem():
    """
    Representation of a problem. This class is used to store the problem information in a format
    that is recognized by the rendering engine.

    :param name: Name of the problem.
    :type name: str
    :param grade: Grade of the problem.
    :type grade: str
    :param moves: List of moves of the problem.
    :type moves: List[Move]
    :param is_benchmark: Whether this problem is a benchmark problem.
    :type is_benchmark: bool
    """

    def __init__(self, name: str, grade: str, moves: List[Move], is_benchmark: bool, **kw) -> None:
        """
        Initialize a new Problem instance.
        """
        # Min params
        self.name = name
        self.grade = grade
        self.moves = moves
        self.is_benchmark = is_benchmark
        self.__dict__.update(kw)
