from enum import Enum


class Action(Enum):
    """Models all possible actions."""
    up: int = 0
    down: int = 1
    right: int = 2
    left: int = 3
