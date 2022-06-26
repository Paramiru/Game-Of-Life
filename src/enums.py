from enum import Enum, unique

@unique
class InitialState(Enum):
    RANDOM = 1
    BLINKER = 2
    GLIDER = 3
