import pygame
from typing import List, TYPE_CHECKING

from .game_state import GameState
from ..core import OverlayType, Piece, Board, PieceBag

if TYPE_CHECKING:
    from src.core.game import Game

class PlayState(GameState):
    """
    Estado principal del juego donde ocurren todas las acciones del Tetris.

    Coordina la interacción entre el tablero (Board), el generador de piezas
    (PieceBag) y la entrada del usuario.
    """
    def __init__(self, game: "Game"):
        super().__init__(game)

        self.fall_timer = 0.0
        self.fall_delay = 0.3

        self.lock_delay = 0.05
        self.lock_timer = 0.0

        self.bag = None
        self.current_piece = None
        self.next_pieces = []

    def on_enter(self) -> None:
        rm = self.game.resource_manager

        self.bag = PieceBag(21)

        board_surface = rm.get_image("Board")

        sheet = rm.get_spritesheet("BlocksType")
        block_surface = sheet.get_frames_at_col(0)[0]

        self.board = Board(board_surface=board_surface, block_surface=block_surface)

        self.current_piece = self.bag.get_next_piece()
        # Para mostrar las proximas 3 piezas, luego veo como lo coloco en la ventana
        # self.next_pieces = self.bag.peek_next(3)

        piece_data = rm.get_piece(self.current_piece)
        piece = Piece(self.current_piece, piece_data)

        self.board.spawn_piece(piece)

    def on_exit(self) -> None:
        return
    
    def handle_input(self, events: List[pygame.event.Event]) -> None:
        if self.game.input.is_key_pressed("play", "move_left"):
            if self.board.try_move(0, -1):
                self.lock_timer = 0.0
        if self.game.input.is_key_pressed("play", "move_right"):
            if self.board.try_move(0, 1):
                self.lock_timer = 0.0
        if self.game.input.is_key_pressed("play", "move_down"):
            if self.board.try_move(1, 0):
                self.lock_timer = 0.0
        if self.game.input.is_key_pressed("play", "rotate_piece_right"):
            if self.board.try_rotate(1):
                self.lock_timer = 0.0
        if self.game.input.is_key_pressed("play", "lock_piece"):
            while self.board.try_fall_piece():
                pass
            self.board.lock_piece()
            lines_cleared = self.board.clear_lines()
            self.lock_timer = 0.0
        return 
    
    def render(self, surface: pygame.Surface) -> None:
        surface.fill((30, 30, 30))
        self.board.draw(surface) 
    
    def update(self, dt: float) -> None:
        # --- Genera una nueva pieza ---
        if not self.board.active_piece and self.bag is not None:
            piece_name = self.bag.get_next_piece()
            piece_data = self.game.resource_manager.get_piece(piece_name)
            piece = Piece(piece_name, piece_data)
            
            self.board.spawn_piece(piece)

            if self.board.is_game_over():
                print("Game Over.")
            return

        # --- Caída por gravedad ---
        self.fall_timer += dt

        if self.fall_timer >= self.fall_delay:
            self.fall_timer = 0.0
            
            if self.board.try_fall_piece():
                self.lock_timer = 0.0
            else:
                self.lock_timer += dt
                
                if self.lock_timer >= self.lock_delay:
                    self.board.lock_piece()
                    lines_cleared = self.board.clear_lines()
                    self.lock_timer = 0.0
    
    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False