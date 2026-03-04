from pygame import Surface
from typing import TYPE_CHECKING
from src.constants import PIECE_DEFINITIONS, ROWS, COLS, BLOCK_W, BLOCK_H, PIECE_SPAWN_OFFSET
from src.core.piece_bag import PieceBag
from src.core.board import Board
from src.core.piece import Piece
from src.core.score import Score
from src.core.pieces_preview import PiecesPreview
from src.core.piece_mechanics import PieceMechanics
from src.core.strategy import create_gravity, create_lock
from datetime import date

if TYPE_CHECKING:
    from src.core.types import BoardType, PiecesPreviewType, PieceDataType
    from src.config.gameplay import GameplayRulesetType, GameplayConfigType
    from pygame.font import Font
    from src.database import RawRecord

class GameBoardController:
    """
    Facade del tablero de juego.

    Coordina Board, Piece, PieceBag, Score, PiecesPreview y PieceMechanics.
    Es la única interfaz que PlayState conoce.
    """

    def __init__(self,
                 session_config: "GameplayConfigType",
                 ruleset: "GameplayRulesetType",
                 pieces: "PieceDataType",
                 board: "BoardType",
                 preview: "PiecesPreviewType") -> None:

        self._data          = pieces
        self._game_over     = False
        self._hold_enabled  = ruleset.get("hold", False)
        self._piece:         Piece | None = None
        self._hold_piece:    Piece | None = None
        self._last_action_was_rotation: bool = False

        gravity     = create_gravity(ruleset, session_config)
        lock        = create_lock(ruleset, session_config)
        wall_kicks  = ruleset.get("wall_kicks", False)

        self._score     = Score(session_config)
        self._bag       = PieceBag(PIECE_DEFINITIONS, session_config["general"]["bag_size"])
        self._board     = Board(ROWS, COLS, board["surface"], BLOCK_W, BLOCK_H, board["pos_x"], board["pos_y"])
        self._preview   = PiecesPreview(data=pieces, bag=self._bag, preview=preview)
        self._mechanics = PieceMechanics(gravity, lock, self._board, wall_kicks=wall_kicks)


    @property 
    def current_score(self) -> int:
        return self._score.current_score
    
    @property
    def final_stats(self) -> "RawRecord":
        """Retorna las stats finales para construir un Record."""
        return {
            "score":    self._score.current_score,
            "lines":    self._score.lines_cleared_total,
            "level":    self._score.level,
            "tetrises": self._score.tetrises,
            "date": date.today().isoformat()
        }
    
    # --- CICLO DE JUEGO ---
    def start(self) -> None:
        """Inicia la partida generando la primera pieza."""
        self._spawn_piece()

    def update(self, dt: float) -> None:
        """Actualiza la lógica del tablero: mecánicas, lock y spawn."""
        if self._game_over:
            return

        if self._piece is None or self._piece.is_locked():
            self._spawn_piece()
            if self._is_spawn_blocked():
                self._game_over = True
            return

        self._mechanics.calculate_ghost(self._piece)

        if self._mechanics.update(dt, self._score.level, self._piece):
            self._resolve_lock()

    def draw(self, surface: Surface, pieces: "PieceDataType") -> None:
        """
        Dibuja todos los elementos visuales del tablero.

        Orden: tablero -> preview -> hold -> ghost -> pieza activa.
        """
        self._board.draw(surface, pieces)

        for surf, x, y in self._preview.get():
            surface.blit(surf, (x, y))

        if self._hold_piece is not None:
            hold_surface = self._data[self._hold_piece.name]["surfaces"]["normal"]
            surface.blit(hold_surface, (0, 0))  # (!) posición provisional

        if self._piece is not None and not self._piece.is_locked():
            pos_normal = self._board.get_pixels_of_cell(self._piece.row, self._piece.col)
            pos_ghost  = self._board.get_pixels_of_cell(self._piece.ghost_row, self._piece.ghost_col)
            self._piece.draw_ghost(surface, pos_ghost)
            self._piece.draw_normal(surface, pos_normal)



    # --- INPUT ---

    def move_left(self) -> None:
        if self._piece is None or self._piece.is_locked():
            return
        if self._mechanics.try_move(self._piece, 0, -1):
            self._last_action_was_rotation = False
            self._mechanics.on_move()

    def move_right(self) -> None:
        if self._piece is None or self._piece.is_locked():
            return
        if self._mechanics.try_move(self._piece, 0, 1):
            self._last_action_was_rotation = False
            self._mechanics.on_move()

    def soft_drop(self) -> None:
        if self._piece is None or self._piece.is_locked():
            return
        if self._mechanics.try_move(self._piece, 1, 0):
            self._score.soft_drop += 1
            self._last_action_was_rotation = False
            self._mechanics.on_move()

    def rotate_right(self) -> None:
        if self._piece is None or self._piece.is_locked():
            return
        if self._mechanics.try_rotate(self._piece, 1):
            self._last_action_was_rotation = True
            self._mechanics.on_move()

    def rotate_left(self) -> None:
        if self._piece is None or self._piece.is_locked():
            return
        if self._mechanics.try_rotate(self._piece, -1):
            self._last_action_was_rotation = True
            self._mechanics.on_move()

    def hard_drop(self) -> None:
        if self._piece is None or self._piece.is_locked():
            return
        self._score.hard_drop = max(0, self._piece.ghost_row - max(self._piece.row, 0))
        self._piece.row = self._piece.ghost_row
        self._piece.col = self._piece.ghost_col
        self._last_action_was_rotation = False
        self._resolve_lock()

    def hold(self) -> None:
        """Guarda la pieza activa y recupera la anterior si el ruleset lo permite."""
        if not self._hold_enabled or self._piece is None or self._piece.is_locked():
            return
        if not self._mechanics.consume_hold():
            return

        if self._hold_piece is None:
            self._hold_piece = Piece(self._piece.name, self._data[self._piece.name])
            self._spawn_piece(enable_hold=False)
        else:
            incoming_name    = self._hold_piece.name
            self._hold_piece = Piece(self._piece.name, self._data[self._piece.name])
            self._piece      = Piece(incoming_name, self._data[incoming_name])
            self._piece.center(self._board.cols, spawn_offset=PIECE_SPAWN_OFFSET)
            self._mechanics.reset()
            self._preview.generate()
            self._mechanics.calculate_ghost(self._piece)



    # --- ESTADO ---

    def is_game_over(self) -> bool:
        return self._game_over

    def debug_draw(self, surface: "Surface", font: "Font") -> None:
        """Delega el debug draw al Score con las métricas internas del controller."""
        fall = (self._mechanics.get_fall_delay(self._score.level), self._mechanics.fall_timer)
        lock = (self._mechanics.lock_delay, self._mechanics.lock_timer)
        self._score.debug_draw(surface, font, fall, lock)

    # --- HELPERS INTERNOS ---

    def _detect_move_type(self) -> str:
        """Detecta el tipo de jugada al bloquear la pieza."""
        if self._piece is None or not self._last_action_was_rotation:
            return "normal"
        return self._board.detect_t_spin(self._piece)

    def _is_spawn_blocked(self) -> bool:
        """Retorna True si la pieza recién spawneada no puede bajar ni una fila."""
        if self._piece is None:
            return False
        return not self._board.is_valid_move(self._piece, self._piece.row + 1, self._piece.col)

    def _spawn_piece(self, enable_hold: bool = True) -> None:
        """Genera y coloca una nueva pieza en el tablero."""
        piece_name  = self._bag.get_next_piece()
        self._piece = Piece(piece_name, self._data[piece_name])
        self._piece.center(self._board.cols, spawn_offset=PIECE_SPAWN_OFFSET)
        self._mechanics.reset()
        if enable_hold:
            self._mechanics.enable_hold()
        self._preview.generate()
        self._mechanics.calculate_ghost(self._piece)

    def _resolve_lock(self) -> None:
        """Bloquea la pieza activa, limpia líneas y actualiza el score."""
        if self._piece is None:
            return
        move_type = self._detect_move_type()
        self._board.lock_piece(self._piece)
        self._piece.set_locked()
        lines = self._board.clear_lines()
        self._score.update(lines, move_type)
        self._last_action_was_rotation = False
        self._mechanics.reset()

