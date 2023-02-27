from enum import Enum

class GameState(Enum):
    INTRO = 1
    MODE_SELECT = 2
    INTRO_TRANSITION = 3
    GAME = 4
    END = 5
    QUIT = 6
