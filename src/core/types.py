from pygame import Surface
from numpy import ndarray
from typing import TypedDict
         
class PieceSurfaces(TypedDict):
    normal: Surface
    placed: Surface
    ghost: Surface

class BlockSurfaces(TypedDict):
    normal: Surface
    placed: Surface
    ghost: Surface

class PieceData(TypedDict):
    matrices: list[ndarray] # List de matrices con sus rotaciones correspondientes
    surfaces: PieceSurfaces # Dic de Surfaces de la pieza en sus diferentes estados
    block: BlockSurfaces # Dic de Surface del bloque que forma la pieza en sus diferentes estados
    type: int # Int que identifica el color de la pieza para dibujar la Board

PieceDataType = dict[str, PieceData]

class BoardType(TypedDict):
    surface: Surface
    pos_x: int
    pos_y: int

class PiecesPreviewType(TypedDict):
    pos_x: int
    pos_y: int
    max_width: int
    preview_count: int
    margin: int