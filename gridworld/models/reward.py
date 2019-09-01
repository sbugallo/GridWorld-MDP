from enum import Enum


class Reward(Enum):
    """Models all possible rewards."""
    goal: int = 1
    start: int = 0
    obstacle: int = -1
    road: int = 0
