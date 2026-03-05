from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.core.piece import Piece
    from src.core.board import Board
    from src.core.strategy import GravityStrategy, LockStrategy


class PieceMechanics:
    """
    Gestiona las mecánicas de la pieza activa: caída por gravedad, bloqueo,
    posición fantasma, movimiento y rotación.

    Mantiene referencia al tablero ya que es una instancia única durante toda la partida.
    La pieza se recibe por argumento en cada llamada ya que cambia en cada spawn.
    """

    def __init__(self, gravity: "GravityStrategy", lock: "LockStrategy", board: "Board", wall_kicks: bool = False) -> None:
        """
        Args:
            gravity:    Estrategia de gravedad activa.
            lock:       Estrategia de bloqueo activa.
            board:      Tablero de juego, instancia única durante la partida.
            wall_kicks: Si se aplican wall kicks al rotar.
        """
        self._gravity           = gravity
        self._lock              = lock
        self._board             = board
        self._wall_kicks        = wall_kicks
        self._fall_timer: float = 0.0
        self._can_hold: bool    = False

    @property
    def lock_delay(self) -> float:
        return self._lock.delay

    @property
    def lock_timer(self) -> float:
        return self._lock.timer

    @property
    def fall_timer(self) -> float:
        return self._fall_timer

    def get_fall_delay(self, level: int) -> float:
        """Retorna el delay de caída según el nivel actual."""
        return self._gravity.get_fall_delay(level)

    def update(self, dt: float, level: int, piece: "Piece") -> bool:
        """
        Actualiza la gravedad y el lock de la pieza activa.

        Args:
            dt:    Delta time en segundos.
            level: Nivel actual para calcular la gravedad.
            piece: Pieza activa.

        Returns:
            True si la pieza debe bloquearse este frame.
        """
        # Caída por gravedad
        self._fall_timer += dt
        if self._fall_timer >= self.get_fall_delay(level):
            if self._board.is_valid_move(piece, piece.row + 1, piece.col):
                piece.move(1, 0)
            self._fall_timer = 0.0

        # Actualizar lock
        is_colliding = not self._board.is_valid_move(piece, piece.row + 1, piece.col)
        self._lock.update(dt, is_colliding)

        return is_colliding and self._lock.is_locked()

    def calculate_ghost(self, piece: "Piece") -> None:
        """
        Calcula y actualiza la posición fantasma de la pieza.

        Solo recalcula si la columna o rotación cambiaron desde el último cálculo.

        Args:
            piece: Pieza activa.
        """
        if piece.col == piece.ghost_col and piece.rot == piece.ghost_rot and piece.row == piece.ghost_row:
            return

        row = piece.row
        while self._board.is_valid_move(piece, row + 1, piece.col):
            row += 1

        piece.ghost_row = row
        piece.ghost_col = piece.col
        piece.ghost_rot = piece.rot

    def try_move(self, piece: "Piece", dr: int, dc: int) -> bool:
        """
        Intenta mover la pieza en la dirección indicada.

        Args:
            piece: Pieza activa.
            dr:    Desplazamiento vertical.
            dc:    Desplazamiento horizontal.

        Returns:
            True si el movimiento fue válido y se aplicó.
        """
        if piece.is_locked():
            return False
        if self._board.is_valid_move(piece, piece.row + dr, piece.col + dc):
            piece.move(dr, dc)
            return True
        return False

    def try_rotate(self, piece: "Piece", direction: int) -> bool:
        """
        Intenta rotar la pieza aplicando wall kicks.

        Args:
            piece:     Pieza activa.
            direction: 1 para horario, -1 para antihorario.

        Returns:
            True si la rotación fue válida y se aplicó.
        """
        if piece.is_locked() or piece.name == "O":
            return False

        old_rot = piece.rot
        old_row = piece.row
        old_col = piece.col

        piece.rotate(direction)

        # Los wall kicks SRS están en formato (x, y) donde:
        # x = desplazamiento de columna (positivo = derecha)
        # y = desplazamiento de fila SRS (positivo = arriba), invertido para pygame
        kicks = piece.get_wall_kicks(old_rot, piece.rot) if self._wall_kicks else [(0, 0)]

        for dx, dy in kicks:
            if self._board.is_valid_move(piece, old_row - dy, old_col + dx):
                piece.move(-dy, dx)
                return True

        # Revertir si todos los wall kicks fallan
        piece.rot = old_rot
        piece.row = old_row
        piece.col = old_col
        return False

    def on_move(self) -> None:
        """Notifica al lock que la pieza se movió o rotó."""
        self._lock.on_move()

    def enable_hold(self) -> None:
        """Activa el hold para la pieza actual."""
        self._can_hold = True

    def consume_hold(self) -> bool:
        """
        Intenta consumir el hold disponible.

        Returns:
            True si el hold estaba disponible y se consumió.
        """
        if not self._can_hold:
            return False
        self._can_hold = False
        return True

    def reset(self) -> None:
        """Resetea los timers al spawnear una nueva pieza."""
        self._fall_timer = 0.0
        self._lock.reset_timer()