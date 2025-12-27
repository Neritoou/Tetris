from pygame import Surface
from typing import List, TypedDict
from numpy import ndarray
from enum import Enum, auto


class PieceSurfaces(TypedDict):
    normal: Surface
    placed: Surface
    ghost: Surface


class PieceData(TypedDict):
    matrices: List[ndarray]
    surfaces: PieceSurfaces


class OverlayType(Enum):
    NONE = auto()           # No es overlay, es parte del flujo principal
    SEMITRANSPARENT = auto()  # Overlay que permite renderizar estados debajo
    FULLSCREEN = auto()       # Overlay que ocupa toda la pantalla, no renderiza fondo