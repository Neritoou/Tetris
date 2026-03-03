from enum import Enum, auto

class StateID(Enum):
    MENU = auto()
    COUNTDOWN = auto()
    PLAY = auto()
    PAUSE = auto()
    GAME_OVER = auto()
    # Más estados

# ENUM DE OVERLAYS PARA LOS ESTADOS DEL JUEGO
class OverlayType(Enum):
    NONE = auto()           # No es overlay, es parte del flujo principal
    SEMITRANSPARENT = auto()  # Overlay que permite renderizar estados debajo
    FULLSCREEN = auto()       # Overlay que ocupa toda la pantalla, no renderiza fondo