from enum import Enum, auto
from pygame import Surface
from numpy import ndarray
from typing import List, TypedDict

# ENUM DE OVERLAYS PARA LOS ESTADOS DEL JUEGO
class OverlayType(Enum):
    NONE = auto()           # No es overlay, es parte del flujo principal
    SEMITRANSPARENT = auto()  # Overlay que permite renderizar estados debajo
    FULLSCREEN = auto()       # Overlay que ocupa toda la pantalla, no renderiza fondo



# INFORMACIÓN DE TIPAADO PARA LAS PIEZAS DE TETRIS
class PieceSurfaces(TypedDict):
    normal: Surface
    placed: Surface
    ghost: Surface

class PieceData(TypedDict):
    matrices: List[ndarray]
    surfaces: PieceSurfaces