from enum import Enum, auto
from pygame import Surface
from numpy import ndarray
from typing import Dict,List, TypedDict

# ENUM DE OVERLAYS PARA LOS ESTADOS DEL JUEGO
class OverlayType(Enum):
    NONE = auto()           # No es overlay, es parte del flujo principal
    SEMITRANSPARENT = auto()  # Overlay que permite renderizar estados debajo
    FULLSCREEN = auto()       # Overlay que ocupa toda la pantalla, no renderiza fondo
                
class PieceSurfaces(TypedDict):
    normal: Surface
    placed: Surface
    ghost: Surface

class BlockSurfaces(TypedDict):
    normal: Surface
    placed: Surface
    ghost: Surface

class PieceData(TypedDict):
    matrices: List[ndarray] # List de matrices con sus rotaciones correspondientes
    surfaces: PieceSurfaces # Dic de Surfaces de la pieza en sus diferentes estados
    block: BlockSurfaces # Dic de Surface del bloque que forma la pieza en sus diferentes estados
    type: int # Int que identifica el color de la pieza para dibujar la Board

PieceDataType = Dict[str, PieceData]

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