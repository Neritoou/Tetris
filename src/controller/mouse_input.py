import pygame
from typing import Set, Tuple

class MouseInputManager:
    """Manejo de entradas del mouse."""

    def __init__(self):
        # Estados de botones del mouse
        self._pressed: Set[int] = set() 
        self._held: Set[int] = set()  
        self._released: Set[int] = set()  

    @property
    def pressed(self) -> Set[int]:
        return self._pressed
    
    @property
    def held(self) -> Set[int]:
        return self._held
    
    @property
    def released(self) -> Set[int]:
        return self._released
    
    @property
    def pos(self) -> Tuple[int, int]:
        """Obtiene la posición actual del mouse."""
        return pygame.mouse.get_pos()  
    
    def is__pressed(self, button: int) -> bool:
        """Verifica si el botón del mouse está presionado."""
        return button in self._pressed

    def is_held(self, button: int) -> bool:
        """Verifica si el botón del mouse está mantenido."""
        return button in self._held

    def is_released(self, button: int) -> bool:
        """Verifica si el botón del mouse ha sido liberado."""
        return button in self._released

   # Detectar input del Mouse
    def _handle_event(self, event: pygame.event.Event) -> None:
        """Maneja los eventos de mouse (MOUSEBUTTONDOWN, MOUSEBUTTONUP)."""
        button = event.button
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si es la primera vez que se presiona, añadir a _pressed
            if button not in self._held:
                self._pressed.add(button)
            self._held.add(button) # Siempre se marca como "held"

        elif event.type == pygame.MOUSEBUTTONUP:
            self._released.add(button) # Marcar como liberado
            self._held.discard(button) # Eliminar de los mantenidos 