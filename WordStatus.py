from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class WordStatus:
    """
    Status legend:  
        0 = Correct\n
        1 = Wrong\n
        2 = Wrong Position
    """
    status: List[int]
    word: str
