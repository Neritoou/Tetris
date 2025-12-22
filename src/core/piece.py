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
            rot (int): Indice de la rotacion actual.
            data (PieceData): Datos estaticos de la pieza (matrices y superficies.
            state (str): Estado visual de la pieza (normal, placed, ghost)
        """

        self.name = name
        self.row = row
        self.col = col
        self.rot = rot
        self.data = data
        self.state = state

    @property
    def matrix(self) -> np.ndarray:
        """Devuelve la matriz correspondiente a la rotacion actual de la pieza"""
        return self.data["matrices"][self.rot]

    @property
    def image(self):
        """Devuelve la imagen de la pieza segun su estado visual"""
        return self.data["surfaces"][self.state]

    def move(self, dr: int, dc: int):
        """
        Modifica la posicion de la pieza desplazandola en filas y columnas.

        Args:
            dr: Desplazamiento vertical (filas)
            dc: Desplazamiento horizontal (columnas)
        """
        
        self.row += dr
        self.col += dc

    def rotate(self, direction: int = 1): 
        """
        Actualiza la rotacion de la pieza
        
        Args:
            direction: Direccion de la rotacion, predeterminado para rotacion en el sentido horaria.
        """
        
        total = len(self.data["matrices"]) # mide la cantidad de rotaciones que tiene la pieza
        self.rot = (self.rot + direction) % total # se le suma una rotacion a la actual y se aplica el mod para que vuelva a 0 si alcanza el limite


    def draw(self, surface: pygame.Surface):
        """
        Dibuja la pieza en la superficie indicada segun la posicion actual
        
        Args:
            surface: Superficie sobre la que se dibuja la pieza.
        """

        x = self.col * BLOCK_W
        y = self.row * BLOCK_H
        surface.blit(self.image, (x, y))

    def get_cells(self) -> list[tuple[int, int]]:
        """Calcula las coordenadas de las celdas ocupadas por la pieza."""
        
        cells = []
        matrix = self.matrix

        for r in range(len(matrix)): # itera con respecto a las filas
            for c in range(len(matrix[r])): # itera con respecto a las columnas que tenga la fila actual
                if matrix[r][c]:
                    cells.append(self.row + r, self.col + c)
        return cells