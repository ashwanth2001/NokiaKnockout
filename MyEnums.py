from enum import Enum

class GameState(Enum):
    INTRO = 1
    INTRO_TRANSITION = 2
    GAME = 3
    END = 4
