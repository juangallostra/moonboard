from dataclasses import dataclass
from typing import List

@dataclass
class Setter:
    nickname: str
    firstname: str
    lastname: str

@dataclass
class Move:
    id: int
    description: str
    is_start: bool = False
    is_end: bool = False

class Problem():
    def __init__(self, name:str, grade:str, moves:List[Move], is_benchmark:bool, **kw) -> None:
        # Min params
        self.name = name
        self.grade = grade
        self.moves = moves
        self.is_benchmark = is_benchmark
        self.__dict__.update(kw)

