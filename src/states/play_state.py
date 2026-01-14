import pygame
from typing import List, TYPE_CHECKING
from .game_state import GameState
from ..core import OverlayType, GameBoardController
from ..constants import BOARD_X, BOARD_Y
from .state_id import StateID
from ..core.strategy import create_gravity, create_lock

if TYPE_CHECKING:
    from src.core.game import Game
    from ..core.types import PieceDataType, BoardType, PiecesPreviewType
    from ..config.gameplay import GameplayConfigType, GameplayRulesetType
    from ..core.strategy import LockStrategy, GravityStrategy

class PlayState(GameState):
    """
    Estado principal del juego donde ocurren todas las acciones del Tetris.

    Coordina la interacción entre el tablero (Board), el generador de piezas
    (PieceBag) y la entrada del usuario.
    """
    def __init__(self, game: "Game", session_data: "GameplayConfigType", ruleset: "GameplayRulesetType"):
        super().__init__(game)
        self._started = False
        self._pause = False
        self._game_over = False
        self.session_config = session_data
        
        self.gravity: GravityStrategy = create_gravity(ruleset, session_data)
        self.lock: LockStrategy = create_lock(ruleset, session_data)
        self.fall_timer = 0.0
        
        # (!) LA FONT ES DE PRUEBA
        self.font = pygame.font.SysFont("Consolas", 20)
        self.pieces: "PieceDataType" 
        self.session: GameBoardController

        #self.next_pieces = [] # (!) Ver que se hará con esto
    
    # (!) CAMBIAR LUEGO FALL Y LOCK DELAY A SESSION
    @property
    def fall_delay(self) -> float:
        return self.gravity.get_fall_delay(self.session.score.level)
    
    def on_enter(self) -> None:
        self.pieces =  self.game.resources.get_pieces()
        board_surface = self.game.resources.get_image("Board")

        board_config: "BoardType" = {"surface": board_surface, "pos_x": BOARD_X, "pos_y": BOARD_Y}
        preview_config: "PiecesPreviewType" =  {"pos_x": BOARD_X + board_surface.get_width() + 20, "pos_y": BOARD_Y, 
                                                "max_width": 80, "margin": 8, 
                                                "preview_count": self.session_config["general"]["preview_count"]}
        
        self.session = GameBoardController(self.session_config, self.pieces, board_config, preview_config)                                     
        self.game.state.change(StateID.COUNTDOWN, playstate = self)

    def on_exit(self) -> None:
        return
    
    def handle_input(self, events: List[pygame.event.Event]) -> None:
        if not self._started or self._game_over:
            return
        
        if self.game.input.is_key_pressed("play", "move_left"):
            if self.session.try_move_piece_to(0,-1):
                self.lock.on_move()

        if self.game.input.is_key_pressed("play", "move_right"):
            if self.session.try_move_piece_to(0,1):
                self.lock.on_move()

        if self.game.input.is_key_pressed("play", "move_down"):
            if self.session.try_soft_drop_piece():
                self.lock.on_move()

        if self.game.input.is_key_pressed("play", "rotate_piece_right"):
            if self.session.try_rotate_piece(1):
                self.lock.on_move()

        if self.game.input.is_key_pressed("play", "rotate_piece_left"):
            if self.session.try_rotate_piece(-1):
                self.lock.on_move()

        if self.game.input.is_key_pressed("play", "hard_drop"):
            self.session.try_hard_drop_piece()
            self._lock_piece()
    
    def render(self, surface: pygame.Surface) -> None:
        surface.fill((30, 30, 30))
        self.session.draw(self.game.surface, self.pieces)
        self.session.score.debug_draw(self.game.surface,self.font,(self.fall_delay, self.fall_timer),(self.lock.delay, self.lock.timer))

    def update(self, dt: float) -> None:
        if not self._started or self._game_over:
            return

        # --- Genera nueva pieza si la anterior está bloqueada ---
        if self.session.piece.is_locked():
            self.session.spawn_piece()
            if self.is_game_over():
                self._game_over = True
                print("Game Over.")
            return

        # --- Actualiza la caída ---
        self.fall_timer += dt
        if self.fall_timer >= self.fall_delay:
            self.fall_timer = 0.0
            self.session.try_fall_piece()
                
        # --- Actualiza el lock ---
        is_colliding = not self.session.can_piece_move(1,0)
        self.lock.update(dt, is_colliding)

        # --- Bloquea la pieza si está colisionando ---
        if is_colliding and self.lock.is_locked():
            self._lock_piece()
    
    def is_game_over(self) -> bool:
        """Verifica si la pieza recién generada colisiona de inmediato."""
        return not self.session.can_piece_move(1, 0)
    
    def _start_game(self):
        self._started = True
        self.session.spawn_piece()
        
    def _lock_piece(self):
        data = self.session.resolve_piece_lock()
        self.lock.timer = 0.0
        self.session.score.update(
            data["lines_cleared"],
            data["type"],
            data["soft_drop"],
            data["hard_drop"]
        )

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False