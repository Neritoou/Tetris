import pygame
from typing import List, TYPE_CHECKING
from ..util import OverlayType
from .game_state import GameState

from ..core.piece import Piece
from ..core.board import Board


if TYPE_CHECKING:
    from src.core.game import Game



class PlayState(GameState):
    def __init__(self, game: "Game"):
        super().__init__(game)

    def on_enter(self) -> None:
        rm = self.game.resource_manager

        piece_data = rm.get_piece("T")
        self.piece = Piece("T", piece_data)
        
        grid_surface = rm.get_image("Board")
        block_surface = piece_data["surfaces"]["placed"]

        self.board = Board(grid_surface=grid_surface, block_surface=block_surface)
        self.board.x = (1084 - self.board.width) // 2
        self.board.y = (720 - self.board.height) // 2

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
        surface.fill((30, 30, 30))
        self.board.draw(surface)
        self.piece.draw(surface)
    
    def update(self, dt: float) -> None:
        return
    
    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False