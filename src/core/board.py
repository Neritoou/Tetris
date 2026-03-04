import pygame
import numpy as np
from typing import TYPE_CHECKING
from src.constants import NUM_TO_PIECE

if TYPE_CHECKING:
    from piece import Piece
    from src.core.types import PieceDataType

class Board:
    """
    Gestiona la lógica y el estado del tablero de juego.

    Es responsable de mantener la matriz de bloques fijos, controlar 
    el movimiento y rotación de la pieza activa mediante validaciones de 
    colisión y procesar la eliminación de líneas completas.
    """
    ANIM_STEP_DURATION = 0.08
    def __init__(self, rows: int, cols: int, surface: pygame.Surface, 
                 cell_width: int, cell_height: int,
                 pos_x: int, pos_y: int) -> None:
        """
        Inicializa el tablero del juego.

        Args:
            surface: Imagen del tablero.
            block_surface: Bloque individual de cada pieza.
        """
        self.rows = rows
        self.cols = cols
        self.matrix: np.ndarray = np.zeros((self.rows, self.cols), dtype=int)

        self._surface = surface
        self._width: int = self._surface.get_width()
        self._height: int = self._surface.get_height()
        self._rect: pygame.Rect = self._surface.get_rect()
        self._rect.topleft = (pos_x, pos_y)

        self.cell_width = cell_width
        self.cell_height = cell_height


        # Animación de eliminación de líneas
        self._anim_rows:  list[int] = []
        self._anim_set:   set[int]  = set()
        self._anim_step:  int       = 0
        self._anim_timer: float     = 0.0
        self._anim_total: int       = cols // 2

    @property
    def is_animating(self) -> bool:
        """True mientras haya una animación de eliminación de filas en curso."""
        return bool(self._anim_rows)
    
    def update(self, dt: float) -> None:
        """
        Avanza la animación activa.

        Cuando la animación termina, aplica la eliminación real de filas
        y limpia el estado de animación.
        """
        if not self._anim_rows:
            return

        self._anim_timer += dt
        if self._anim_timer >= self.ANIM_STEP_DURATION:
            self._anim_timer -= self.ANIM_STEP_DURATION
            self._anim_step  += 1

            if self._anim_step >= self._anim_total:
                self.__remove_filled_lines(np.array(self._anim_rows))
                self._anim_rows  = []
                self._anim_set   = set()
                self._anim_step  = 0
                self._anim_timer = 0.0

    def draw(self, surface: pygame.Surface, pieces: "PieceDataType") -> None:
        """Dibuja el fondo del tablero, los bloques estáticos y la pieza activa."""
        # Dibuja la Board
        surface.blit(self._surface, self._rect)
        center = self.cols // 2

        for (row,col), block in np.ndenumerate(self.matrix):
            if not block:
                continue
            if (self._anim_rows
                    and row in self._anim_set
                    and center - self._anim_step <= col <= center + self._anim_step - 1):
                continue

            bx = self._rect.x + col * self.cell_width
            by = self._rect.y + row * self.cell_height
            surface.blit(pieces[NUM_TO_PIECE[block]]["block"]["placed"], (bx, by))

    def lock_piece(self, piece: "Piece") -> None:
        """
        Bloquea la pieza actual en el tablero, marcando las celdas que ocupa como ocupadas 
        (con valor 1) en la matriz. Después de bloquearla, la pieza activa se elimina.
        """
        for r, c in piece.get_cells():
            # Verifica que la celda esté dentro del tablero
            if 0 <= r < self.rows and 0 <= c < self.cols: 
                self.matrix[r, c] = piece.type

    def clear_lines(self) -> int:
        """
        Detecta las filas completas e inicia la animación de eliminación.

        La remoción real de la matriz ocurre al finalizar la animación (ver update).
        El conteo se devuelve de inmediato para que Score calcule los puntos sin esperar.

        Returns:
            int: Cantidad de líneas detectadas (0 si no hay ninguna).
        """
        fullrows = self.__find_fullrows()

        if len(fullrows) == 0:
            return 0

        self._anim_rows  = list(fullrows)
        self._anim_set   = set(fullrows)
        self._anim_step  = 0
        self._anim_timer = 0.0

        return len(fullrows)
    
    def is_valid_move(self, piece: "Piece", row: int | None = None, col: int | None = None) -> bool:
        """
        Verifica si la pieza colisiona con los bordes o bloques existentes.

        Args:
            piece: Instancia de la pieza a validar.
            row: Posición de la pieza en las filas del tablero.
            col: Posición de la pieza en las columnas del tablero.

        Returns:
            bool: True si la posición está libre, False si no está ocupada o fuera de límites.

        """
        for r, c in piece.get_cells(row, col):
            if r >= self.rows or (c < 0 or c >= self.cols) or (r >= 0  and self.matrix[r, c]):
                return False
        return True
    
    def is_empty(self, check_rows: int = 3) -> bool:
        """Verifica si las últimas `check_rows` filas del tablero están vacías.

        Con tan solo comprobar las últimas filas es posible conocer si la Board está vacía"""
        return not np.any(self.matrix[-check_rows:, :])


    def detect_t_spin(self, piece: "Piece") -> str:
        if piece.name != "T":
            return "normal"

        cr = piece.row + 1
        cc = piece.col + 1

        corners = [
            (cr - 1, cc - 1),  # TL
            (cr - 1, cc + 1),  # TR
            (cr + 1, cc - 1),  # BL
            (cr + 1, cc + 1),  # BR
        ]

        front_corners = {
            0: (corners[0], corners[1]),  # rot 0 → arriba:    TL, TR
            1: (corners[1], corners[3]),  # rot 1 → derecha:   TR, BR
            2: (corners[2], corners[3]),  # rot 2 → abajo:     BL, BR
            3: (corners[0], corners[2]),  # rot 3 → izquierda: TL, BL
        }

        occupied = [self._is_corner_occupied(r, c) for r, c in corners]
        count    = sum(occupied)

        f1, f2         = front_corners[piece.rot % 4]
        both_front     = self._is_corner_occupied(*f1) and self._is_corner_occupied(*f2)

        if count >= 3:
            # T-spin propio: ambas esquinas frontales bloqueadas
            # Mini T-spin:   solo una esquina frontal bloqueada (imposible con 4, pero válido con 3)
            return "t_spin" if both_front else "mini_t_spin"

        if count == 2 and both_front:
            return "mini_t_spin"

        return "normal"


    
    # --- HELPERS ---
    def _is_corner_occupied(self, r: int, c: int) -> bool:
        """Retorna True si la celda está fuera del tablero o tiene un bloque."""
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            return True
        return bool(self.matrix[r, c])
    
    def get_pixels_of_cell(self, row: int, col: int) -> tuple[int, int]:
        """
        Convierte una posición de celda del tablero (row, col) en coordenadas
        absolutas en píxeles para dibujar la pieza en pantalla.

        La conversión toma como origen la esquina superior izquierda del tablero
        y aplica el tamaño de cada celda.

        Args:
            row: Fila de la celda dentro del tablero.
            col: Columna de la celda dentro del tablero.

        Returns:
            Tuple[int, int]: Coordenadas (x, y) en píxeles dentro de la ventana.
        """
        return ((self._rect.x + col * self.cell_width), (self._rect.y + row * self.cell_height))
    
    def __find_fullrows(self) -> np.ndarray:
        """
        Encuentra las filas llenas en el tablero (todas las celdas tienen un valor diferente de 0).

        Returns:
            np.ndarray: Un arreglo con los índices de las filas completas.
        """
        # Verifica si todas las celdas en cada fila son diferentes de 0
        fullrows = np.where(np.all(self.matrix != 0, axis=1))[0]
        return fullrows
    
    def __remove_filled_lines(self, fullrows: np.ndarray) -> None:
        """
        Elimina las filas llenas de la matriz y las desplaza hacia abajo.

        Args:
            fullrows: Las filas que deben ser eliminadas.
        """
        # Elimina las filas completas de la matriz
        self.matrix = np.delete(self.matrix, fullrows, axis=0)

        # Añade filas vacías (llenas de ceros) en la parte superior del tablero
        new_emptyrows = np.zeros((len(fullrows), self.cols), dtype=int) # Crea las filas vacias
        self.matrix = np.vstack((new_emptyrows, self.matrix)) # Las anexa a la matrix