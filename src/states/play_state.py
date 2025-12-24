import pygame
from typing import List, TYPE_CHECKING
from ..util import OverlayType
from .game_state import GameState


if TYPE_CHECKING:
    from src.core.game import Game



class PlayState(GameState):
    def __init__(self, game: "Game"):
        super().__init__(game)

    def on_enter(self) -> None:
        return 
    
    def on_exit(self) -> None:
        return
    
    def handle_input(self, events: List[pygame.event.Event]) -> None:
        if self.game.input.is_mouse_released("left"):
            print("ESTAS PRESIONANDO MOVE_LEFT")
            print("------------------")
        if self.game.input.is_key_held("play","move_right"):
            print("ESTAS HOLDEANDO LA W")
            print("-------------------")
        return 
    
    def render(self, surface: pygame.Surface) -> None:
        return 
    
    def update(self, dt: float) -> None:
        return
    
    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False