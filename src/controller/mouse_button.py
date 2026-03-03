from enum import Enum
from pygame import BUTTON_LEFT, BUTTON_MIDDLE, BUTTON_RIGHT, BUTTON_WHEELDOWN, BUTTON_WHEELUP

class MouseButton(Enum):
    LEFT = BUTTON_LEFT
    MIDDLE = BUTTON_MIDDLE
    RIGHT = BUTTON_RIGHT
    SCROLL_UP = BUTTON_WHEELUP
    SCROLL_DOWN = BUTTON_WHEELDOWN
    
    @classmethod
    def from_name(cls, name: str) -> "MouseButton":
        """Convierte nombre a enum."""
        try:
            return cls[name.upper()]
        except KeyError:
            raise ValueError(f"Botón de mouse inválido: '{name}'")
    
    @classmethod
    def from_pygame(cls, button_id: int) -> "MouseButton":
        """Convierte pygame.BUTTON_* a enum."""
        try:
            return cls(button_id)
        except ValueError:
            raise ValueError(f"ID de botón pygame inválido: {button_id}")
