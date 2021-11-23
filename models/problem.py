from dataclasses import dataclass
from typing import List

@dataclass
class Setter:
    """
    Information about the setter of the problem.
    """
    nickname: str
    firstname: str
    lastname: str

@dataclass
class Move:
    """
    Information about a move of thr problem.
    """
    id: int
    row: int
    column: int
    description: str
    is_start: bool = False
    is_end: bool = False

class Problem():
    def __init__(self, name:str, grade:str, moves:List[Move], is_benchmark:bool, **kw) -> None:
        """
        Representation of a problem. This class is used to store the problem information in a format
        that is recognized by the rendering engine.

        Args:
            name (str): Problem name
            grade (str): Problem grade
            moves (List[Move]): List of problem moves
            is_benchmark (bool): Boolean indicating whether the problem is a benchmark
        """
        # Min params
        self.name = name
        self.grade = grade
        self.moves = moves
        self.is_benchmark = is_benchmark
        self.__dict__.update(kw)

