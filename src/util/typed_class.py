from pygame import Surface, BUTTON_LEFT,BUTTON_MIDDLE,BUTTON_RIGHT,BUTTON_WHEELDOWN,BUTTON_WHEELUP
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


class MouseButton(Enum):
    LEFT = BUTTON_LEFT
    MIDDLE = BUTTON_MIDDLE
    RIGHT = BUTTON_RIGHT
    SCROLL_UP = BUTTON_WHEELUP
    SCROLL_DOWN = BUTTON_WHEELDOWN

    @classmethod
    def from_name(cls, name: str) -> "MouseButton":
        """Convierte el nombre de un botón en el correspondiente enum de MouseButton."""
        try:
            return cls[name.upper()]
        except KeyError:
            raise ValueError(f"input Manager: botón del mouse inválido: '{name}'")