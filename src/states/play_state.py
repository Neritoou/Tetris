import pygame
from typing import Dict, Any, List, TYPE_CHECKING

from .game_state import GameState
from ..core import OverlayType, Board, GameBoardController, PieceSpawner, PieceBag, Score
from ..constants import PIECE_DEFINITIONS, ROWS, COLS, BLOCK_W, BLOCK_H, BOARD_X, BOARD_Y

if TYPE_CHECKING:
    from src.core.game import Game
    from ..core.types import PieceData

class PlayState(GameState):
    """
    Estado principal del juego donde ocurren todas las acciones del Tetris.

    Coordina la interacción entre el tablero (Board), el generador de piezas
    (PieceBag) y la entrada del usuario.
    """
    def __init__(self, game: "Game", session_data: Dict[Any, Any]):
        super().__init__(game)

        self.config_session = session_data

        self.fall_timer = 0.0
        self.fall_delay = self.config_session["general"]["fall_delay"]

        self.lock_delay = self.config_session["general"]["lock_delay"]
        self.lock_timer = 0.0
        
        # (!) LA FONT ES DE PRUEBA
        self.font = pygame.font.SysFont("Consolas", 20)
        self.pieces: "Dict[str, PieceData]" 
        self.score: Score
        self.bag: PieceBag
        self.board: Board
        self.session: GameBoardController
        self.data_to_score = Dict[str, Any]

        #self.next_pieces = [] # (!) Ver que se hará con esto

    def on_enter(self) -> None:
        self.pieces =  self.game.resources.get_pieces()
        self.score = Score(self.config_session)
        self.bag = PieceBag(PIECE_DEFINITIONS, 3)
        spawner = PieceSpawner(self.bag, self.pieces)
        board_surface = self.game.resources.get_image("Board")
        self.board = Board(ROWS, COLS, board_surface, BLOCK_W, BLOCK_H, BOARD_X, BOARD_Y)
        self.session = GameBoardController(self.board, spawner, self.score)
        
        self.session.spawn_piece()

    def on_exit(self) -> None:
        return
    
    def handle_input(self, events: List[pygame.event.Event]) -> None:
        if self.game.input.is_key_pressed("play", "move_left"):
            if self.session.try_move_to(0, -1):
                self.lock_timer = 0.0

        if self.game.input.is_key_pressed("play", "move_right"):
            if self.session.try_move_to(0, 1):
                self.lock_timer = 0.0

        if self.game.input.is_key_pressed("play", "move_down"):
            if self.session.try_move_to(1, 0):
                self.lock_timer = 0.0

        if self.game.input.is_key_pressed("play", "rotate_piece_right"):
            if self.session.try_rotate(1):
                self.lock_timer = 0.0

        if self.game.input.is_key_pressed("play", "lock_piece"):
            self.session.try_hard_drop()
            self.data_to_score = self.session.resolve_piece_lock()
            self.score.update(self.data_to_score["lines_cleared"],
                              self.data_to_score["type"],
                              self.data_to_score["soft_drop"],
                              self.data_to_score["hard_drop"]
                              )
            
            self.lock_timer = 0.0

        return 
    
    def render(self, surface: pygame.Surface) -> None:
        surface.fill((30, 30, 30))
        self.session.draw(self.game.surface, self.pieces)
        self.score.debug_draw(self.game.surface,self.font)
    
    def update(self, dt: float) -> None:

        # --- Genera una nueva pieza ---
        if not self.session.piece and self.bag is not None:
            self.session.spawn_piece()

            if self.is_game_over():
                print("Game Over.")
            return

        # --- Caída por gravedad ---
        self.fall_timer += dt
        if self.fall_timer >= self.fall_delay:
            self.fall_timer = 0.0
            
            if self.session.try_fall():
                self.lock_timer = 0.0
                return
            self.lock_timer += dt
                
            if self.lock_timer >= self.lock_delay:
                self.data_to_score = self.session.resolve_piece_lock()
                self.score.update(self.data_to_score["lines_cleared"],
                              self.data_to_score["type"],
                              self.data_to_score["soft_drop"],
                              self.data_to_score["hard_drop"]
                              )
                self.lock_timer = 0.0

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False
    
    def is_game_over(self) -> bool:
        """Verifica si la pieza recién generada colisiona de inmediato."""
        if not self.session.piece:
            return False
        if self.board.is_valid(self.session.piece):
            return False
        return True