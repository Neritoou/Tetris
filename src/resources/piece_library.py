import pygame
import numpy as np
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.types import PieceData, PieceDataType, PieceSurfaces, BlockSurfaces

class PieceLibrary:
    """
    Clase que gestiona todas las piezas del juego, incluyendo sus matrices de rotación
    y las surfaces de cada estado (normal, placed, ghost).

    Esta clase es independiente del gameplay y solo almacena los datos de las piezas.
    """
    def __init__(self) -> None:
        """Inicializa el registro de piezas vacío."""
        self._pieces: "PieceDataType" = {}

    # --- MÉTODOS ACCESIBLES ---
    def register_piece(self,name: str, base_matrix: np.ndarray, blocks: "BlockSurfaces", type: int) -> None:
        """
        Registra una nueva pieza en la biblioteca, generando sus rotaciones y surfaces.

        Args:
            name: Nombre identificador de la pieza.
            base_matrix: Matriz base de la pieza para generar rotaciones.
            blocks: Diccionario con surfaces de cada estado de la pieza.

        Raises:
            ValueError*: Si la pieza ya está registrada.
        """
        self._assert_valid_register(name)

        matrices = self._generate_rotations(base_matrix)

        surfaces: "PieceSurfaces" = {
                "normal": self._build_piece(base_matrix, blocks["normal"]),
                "placed": self._build_piece(base_matrix, blocks["placed"]),
                "ghost": self._build_piece(base_matrix, blocks["ghost"]),
            }

        self._pieces[name] = { "matrices": matrices, "surfaces": surfaces, "block": blocks, "type": type}

    def get_piece(self, name: str) -> "PieceData":
        """Devuelve los datos completos de la pieza."""
        self._assert_valid_piece(name)
        return self._pieces[name]
    
    def get_piece_surface(self, name: str, state: str = "normal") -> pygame.Surface:
        """Obtiene la superficie de la pieza para el estado dado ('normal', 'placed', 'ghost')."""
        self._assert_valid_piece(name)
        if state not in self._pieces[name]["surfaces"]:
            raise ValueError(f"PieceLibrary: la Surface '{state}' de la pieza '{name}' no existe")
        return self._pieces[name]["surfaces"][state]
    
    @property
    def pieces(self) -> "PieceDataType":
        return self._pieces
    


    # --- HELPERS ---
    def _generate_rotations(self, matrix) -> list[np.ndarray]:
        """Genera las cuatro rotaciones (0°, 90°, 180°, 270°) de la matriz."""
        rotations = [matrix]
        for _ in range(3):
            matrix = np.rot90(matrix, k= -1)
            rotations.append(matrix)
        return rotations

    @staticmethod
    def _build_piece(piece_matrix: np.ndarray, block_image: pygame.Surface) -> pygame.Surface:
        """
        Genera la surface de la pieza a partir de la matriz y la imagen del bloque.

        Args:
            piece_matrix: Matriz de la pieza.
            block_image: Surface de un bloque individual.

        Returns:
            pygame.Surface: Surface completa de la pieza.
        """
        # Encuentra los índices de las filas y columnas que contienen bloques
          # Obtener las filas y columnas ocupadas
        rows, cols = piece_matrix.shape  # Desestructurar las dimensiones
        block_w, block_h = block_image.get_size()

        # Buscar las filas y columnas ocupadas por bloques (no vacías)
        occupied_rows = [r for r in range(rows) if np.any(piece_matrix[r, :])]
        occupied_cols = [c for c in range(cols) if np.any(piece_matrix[:, c])]

        # Si no hay filas ni columnas ocupadas, lanzamos un error
        if not occupied_rows or not occupied_cols:
            raise ValueError("Piece Library: No es posible generar una Surface (No se encontraron datos en la matriz).")

        # Calcular las dimensiones reales de la pieza (sin incluir espacios vacíos)
        height = len(occupied_rows) * block_h
        width = len(occupied_cols) * block_w

        # Crear la superficie final con el tamaño correcto (ajustado al contenido)
        piece_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        # Dibujar los bloques en la superficie ajustada
        for (r, c), block in np.ndenumerate(piece_matrix):
            if block:  # Solo dibujar bloques ocupados
                # Calcular las posiciones ajustadas en la nueva surface
                x = (c - occupied_cols[0]) * block_w  # Desplazamos para ajustar al inicio
                y = (r - occupied_rows[0]) * block_h  # Desplazamos para ajustar al inicio
                piece_surface.blit(block_image, (x, y))  # Colocamos el bloque en la surface

        return piece_surface
    
    def _assert_valid_register(self, key: str) -> None:
        """Lanza un ValueError si se intenta registrar una pieza ya cargada."""
        if key in self._pieces:
            raise ValueError(f"PieceLibrary: La pieza '{key}' ya se encuentra Registrada")
        
    def _assert_valid_piece(self, name: str) -> None:
        """Lanza un ValueError si se intenta acceder a una pieza no registrada."""
        if name not in self._pieces:
            raise ValueError(f"PieceLibrary: la pieza '{name}' no se ha Registrado")