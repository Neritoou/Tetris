import pygame
import numpy as np
from constants import BLOCK_H, BLOCK_W
from util import PieceData

class Piece:
    def __init__(self, name: str, row: int, col: int, data: PieceData, rot: int = 0, state: str = "normal"):
        """
        Inicializa una pieza activa del juego.

        Args:
            name (str): Identificador de la pieza ('O', 'T', 'J'...).
            row (int): Fila inicial de la pieza en el tablero.
            col (int): Columna inicial de la pieza en el tablero.
            rot (int): Indice de la rotación actual.
            data (PieceData): Datos estáticos de la pieza (matrices y superficies).
            state (str): Estado visual de la pieza (normal, placed, ghost).
        """

        self.name = name
        self.row = row
        self.col = col
        self.rot = rot
        self.data = data
        self.state = state

    @property
    def matrix(self) -> np.ndarray:
        """Devuelve la matriz correspondiente a la rotación actual de la pieza."""
        return self.data["matrices"][self.rot]

    @property
    def image(self) -> pygame.Surface:
        """Devuelve la imagen de la pieza según su estado visual."""
        return self.data["surfaces"][self.state]

    def move(self, dr: int, dc: int):
        """
        Modifica la posición de la pieza desplazandola en filas y columnas.

        Args:
            dr (int): Desplazamiento vertical (filas).
            dc (int): Desplazamiento horizontal (columnas)
        """
        
        self.row += dr
        self.col += dc

    def rotate(self, direction: int = 1): 
        """
        Actualiza la rotación de la pieza.
        
        Args:
            direction: Dirección de la rotación.
            1 para sentido horario.
            -1 para sentido contrario al horario.
        """
        
        total = len(self.data["matrices"]) # Mide la cantidad de rotaciones que tiene la pieza
        self.rot = (self.rot + direction) % total # Se le suma una rotación a la actual y se aplica el % para controlar el índice de rot


    def draw(self, surface: pygame.Surface):
        x = self.col * BLOCK_W
        y = self.row * BLOCK_H
        surface.blit(self.image, (x, y))

    def get_cells(self, row: int | None = None, col: int | None = None) -> list[tuple[int, int]]:
        """Calcula las coordenadas absolutas de las celdas ocupadas por la pieza."""

        base_row = self.row if row is None else row
        base_col = self.col if col is None else col


        cells = []
        matrix = self.matrix

        for r in range(len(matrix)): # itera con respecto a las filas
            for c in range(len(matrix[r])): # itera con respecto a las columnas que tenga la fila actual
                if matrix[r][c]:
                    cells.append((base_row + r, base_col + c))
        return cells