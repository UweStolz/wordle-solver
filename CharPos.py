from dataclasses import dataclass


@dataclass(frozen=True)
class CharPos:
    position: int
    char: str
