import pygame
from typing import Set, Tuple, TYPE_CHECKING
from ..util.typed_class import MouseButton

class MouseInputManager:
    """Manejo de entradas del mouse."""

    def __init__(self):
        # Estados de botones del mouse
        self._pressed: set[MouseButton] = set()
        self._held: set[MouseButton] = set()
        self._released: set[MouseButton] = set()

    @property
    def pressed(self) -> Set[MouseButton]:
        return self._pressed
    
    @property
    def held(self) -> Set[MouseButton]:
        return self._held
    
    @property
    def released(self) -> Set[MouseButton]:
        return self._released
    
    @property
    def pos(self) -> Tuple[int, int]:
        """Obtiene la posición actual del mouse."""
        return pygame.mouse.get_pos()  
    
    def is_pressed(self, button: str) -> bool:
        """Verifica si un botón del mouse está presionado, usando el nombre del botón."""
        mouse_button = MouseButton.from_name(button)  # Conversión del nombre al enum
        return mouse_button in self._pressed

    def is_held(self, button: str) -> bool:
        """Verifica si un botón del mouse está siendo mantenido, usando el nombre del botón."""
        mouse_button = MouseButton.from_name(button)  # Conversión del nombre al enum
        return mouse_button in self._held

    def is_released(self, button: str) -> bool:
        """Verifica si un botón del mouse ha sido liberado, usando el nombre del botón."""
        mouse_button = MouseButton.from_name(button)  # Conversión del nombre al enum
        return mouse_button in self._released
    
    def is_inside_rect(self, rect: pygame.Rect) -> bool:
        """
        Verifica si el mouse está dentro de un rectángulo.
        rect: (x, y, width, height)
        """
        mx, my = self.pos
        return rect.collidepoint(mx, my)

    def is_pressed_in_rect(self, button: str, rect: pygame.Rect) -> bool:
        """Verifica si un botón está presionado dentro de un rectángulo."""
        return self.is_pressed(button) and self.is_inside_rect(rect)

    def is_held_in_rect(self, button: str, rect: pygame.Rect) -> bool:
        """Verifica si un botón está siendo mantenido dentro de un rectángulo."""
        return self.is_held(button) and self.is_inside_rect(rect)

    def is_released_in_rect(self, button: str, rect: pygame.Rect) -> bool:
        """Verifica si un botón ha sido liberado dentro de un rectángulo."""
        return self.is_released(button) and self.is_inside_rect(rect)
    
    def get_name(self, button: MouseButton) -> str:
        """Obtiene el nombre del botón (izquierdo, derecho, etc.)"""
        return button.name.lower()

   # Detectar input del Mouse
    def _handle_event(self, event: pygame.event.Event) -> None:
        """Maneja los eventos de mouse (MOUSEBUTTONDOWN, MOUSEBUTTONUP)."""
        try:
            button = MouseButton(event.button)  # Conversión de pygame.BUTTON a MouseButton
        except ValueError:
            return  # Si no es un botón reconocido, no lo procesamos.
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si es la primera vez que se presiona, añadir a _pressed
            if button not in self._held:
                self._pressed.add(button)
            self._held.add(button) # Siempre se marca como "held"

        elif event.type == pygame.MOUSEBUTTONUP:
            self._released.add(button) # Marcar como liberado
            self._held.discard(button) # Eliminar de los mantenidos 