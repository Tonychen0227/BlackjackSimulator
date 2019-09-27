from enum import Enum


class Action(Enum):
    STAND = 0
    SURRENDER = 1
    HIT = 2
    SPLIT = 3
    DOUBLE = 4


class Result(Enum):
    LOSS = 0
    PUSH = 1
    WIN = 2
    BLACKJACK = 3
    SURRENDER = 4
