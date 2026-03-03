import pygame
from typing import TYPE_CHECKING
from src.states.game_state import GameState
from src.core import GameBoardController
from src.constants import BOARD_X, BOARD_Y
from src.states.types import StateID, OverlayType

if TYPE_CHECKING:
    from src.core.game import Game
    from src.core.types import PieceDataType, BoardType, PiecesPreviewType
    from src.config.gameplay import GameplayConfigType, GameplayRulesetType

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
        self.session_config = session_data
        
        # (!) LA FONT ES DE PRUEBA
        self.ruleset = ruleset
        self.font = pygame.font.SysFont("Consolas", 20)
        self.pieces: "PieceDataType" 
        self.session: GameBoardController
    
    def on_enter(self) -> None:
        self.pieces =  self.game.resources.get_pieces()
        board_surface = self.game.resources.get_image("Board")

        board_config: "BoardType" = {"surface": board_surface, "pos_x": BOARD_X, "pos_y": BOARD_Y}
        preview_config: "PiecesPreviewType" =  {"pos_x": BOARD_X + board_surface.get_width() + 20, "pos_y": BOARD_Y, 
                                                "max_width": 80, "margin": 8, 
                                                "preview_count": self.session_config["general"]["preview_count"]}
        
        self.session = GameBoardController(self.session_config, self.ruleset, self.pieces, board_config, preview_config)                                     
        self.game.state.change(StateID.COUNTDOWN, playstate = self)

    def on_exit(self) -> None:
        return
    
    def handle_input(self, events: list[pygame.event.Event]) -> None:
        if not self._started or self.game_over:
            return
        
        if self.game.input.is_action_pressed("play", "move_left"):
            if self.session.try_move_piece_to(0,-1):
                self.session.lock.on_move()

        if self.game.input.is_action_pressed("play", "move_right"):
            if self.session.try_move_piece_to(0,1):
                self.session.lock.on_move()

        if self.game.input.is_action_pressed("play", "move_down"):
            if self.session.try_soft_drop_piece():
                self.session.lock.on_move()

        if self.game.input.is_action_pressed("play", "rotate_piece_right"):
            if self.session.try_rotate_piece(1):
                self.session.lock.on_move()

        if self.game.input.is_action_pressed("play", "rotate_piece_left"):
            if self.session.try_rotate_piece(-1):
                self.session.lock.on_move()

        if self.game.input.is_action_pressed("play", "hard_drop"):
            self.session.try_hard_drop_piece()
            self.session.resolve_piece_lock()

        if self.game.input.is_action_pressed("ui", "pause"):
            self.game.state.change(StateID.PAUSE)
            return
    
    def render(self, surface: pygame.Surface) -> None:
        surface.fill((30, 30, 30))
        self.session.draw(self.game.surface, self.pieces)
        self.session.score.debug_draw(self.game.surface,self.font,(self.session.fall_delay, self.session.fall_timer),(self.session.lock.delay, self.session.lock.timer))

    def update(self, dt: float) -> None:
        if not self._started and self.game_over:
            return
        
        self.session.update(dt)

        if self.game_over:
            final_score = self.session.score.current_score
            self.game.state.change(StateID.GAME_OVER, final_score=final_score)
    
    def _start_game(self):
        self._started = True
        self.session.start()


    @property
    def game_over(self) -> bool:
        """Verifica si la pieza recién generada colisiona de inmediato."""
        return self.session.is_game_over()

    @property
    def overlay_type(self) -> OverlayType:
        return OverlayType.NONE

    @property
    def is_transient(self) -> bool:
        return False