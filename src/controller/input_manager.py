import pygame
from typing import List, Tuple
from .key_input import KeyInputManager
from .mapping import KeyMappingManager
from .mouse_input import MouseInputManager

# (!) AÑADIR METODOS PARA LA MODIFICACION DE TECLAS EN OPCIONES

class InputManager:
    """
    Administra el estado de los controles y mapea teclas a acciones semánticas.
    También permite guardar y cargar configuraciones de teclas desde un archivo JSON.
    """
    def __init__(self, config_path: str) -> None:
        self._key = KeyInputManager()  # Maneja eventos del teclado
        self._mouse = MouseInputManager()  # Maneja eventos del mouse
        self._map = KeyMappingManager(config_path)  # Maneja el mapeo de teclas y acciones

    def update(self, events: List[pygame.event.Event]) -> None:
        """Actualiza los estados de las acciones según los eventos del frame."""
        # Limpiar estados previos
        self._key.pressed.clear()
        self._key.released.clear()
        self._mouse.pressed.clear()
        self._mouse.released.clear()

        # Procesa los eventos
        for event in events:
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                self._key._handle_event(event) # Llama a la función que maneja los eventos de teclado
            elif event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                self._mouse._handle_event(event)  # Llama a la función que maneja los eventos del mouse

    # Métodos para acceder a las verificaciones de teclas y mouse
    def is_key_pressed(self, context: str, action: str) -> bool:
        """Verifica si una tecla está presionada para una acción en un contexto específico."""
        return self._key.is_pressed(context, action)

    def is_key_held(self, context: str, action: str) -> bool:
        """Verifica si una tecla está siendo mantenida para una acción en un contexto específico."""
        return self._key.is_held(context, action)

    def is_key_released(self, context: str, action: str) -> bool:
        """Verifica si una tecla ha sido liberada para una acción en un contexto específico."""
        return self._key.is_released(context, action)

    def is_mouse_pressed(self, button: str) -> bool:
        """Verifica si un botón del mouse está presionado."""
        return self._mouse.is_pressed(button)

    def is_mouse_held(self, button: str) -> bool:
        """Verifica si un botón del mouse está siendo mantenido."""
        return self._mouse.is_held(button)

    def is_mouse_released(self, button: str) -> bool:
        """Verifica si un botón del mouse ha sido liberado."""
        return self._mouse.is_released(button)

    def get_mouse_position(self) -> Tuple[int, int]:
        """Obtiene la posición del mouse."""
        return self._mouse.pos
    

