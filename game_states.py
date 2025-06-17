from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    PLAYING = auto()
    COOKING = auto()
    UPGRADE = auto()
    GAME_OVER = auto()
