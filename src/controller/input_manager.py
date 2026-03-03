from src.controller.input_state import InputState
from src.controller.input_mapper import InputMapper
from src.controller.mouse_button import MouseButton
import pygame

class InputManager:
    """
    Manager principal de inputs del juego.
    
    Coordina teclado, mouse y mapeo de acciones.
    """
    def __init__(self, key_map: dict[str, dict[str, set[int]]]):
        """
        Args:
            mapper: InputMapper con la configuración de controles
        """
        # Mapeo Interno
        self._mapper = InputMapper(key_map)

        self._keys = InputState[int]()  # pygame.K_*
        self._mouse = InputState[MouseButton]() # pygame.MOUSE
        self._actions = InputState[tuple[str, str]]()  # (context, action)

    # --- Actualización ---
    def update_controls(self, key_map: dict[str, dict[str, set[int]]]) -> None:
        """Actualiza el mapeo de controles en caliente."""
        self._mapper.update_mapping(key_map)

    def update(self, events: list[pygame.event.Event]) -> None:
        """Procesa eventos del frame."""
        # Limpiar estados transitorios
        self._keys.clear_frame_state()
        self._mouse.clear_frame_state()
        self._actions.clear_frame_state()
        
        # Actualizar posición del mouse
        self._mouse_pos = pygame.mouse.get_pos()
        
        # Procesar eventos
        for event in events:
            if event.type == pygame.KEYDOWN:
                self._handle_key_down(event.key)
            elif event.type == pygame.KEYUP:
                self._handle_key_up(event.key)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._handle_mouse_down(event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._handle_mouse_up(event.button)
    
    def _handle_key_down(self, pygame_key: int) -> None:
        """Maneja tecla presionada."""
        self._keys.handle_down(pygame_key)
        
        # Propagar a acciones lógicas
        for context, action in self._mapper.get_actions_for_key(pygame_key):
            self._actions.handle_down((context, action))
    
    def _handle_key_up(self, pygame_key: int) -> None:
        """Maneja tecla liberada."""
        self._keys.handle_up(pygame_key)
        
        # Propagar a acciones lógicas
        for context, action in self._mapper.get_actions_for_key(pygame_key):
            self._actions.handle_up((context, action))
    
    def _handle_mouse_down(self, button_id: int) -> None:
        """Maneja botón de mouse presionado."""
        try:
            button = MouseButton.from_pygame(button_id)
            self._mouse.handle_down(button)
        except ValueError:
            pass  # Botón no reconocido, ignorar
    
    def _handle_mouse_up(self, button_id: int) -> None:
        """Maneja botón de mouse liberado."""
        try:
            button = MouseButton.from_pygame(button_id)
            self._mouse.handle_up(button)
        except ValueError:
            pass  # Botón no reconocido, ignorar
    
    # --- API de acciones lógicas ---
    def is_action_pressed(self, context: str, action: str) -> bool:
        """Verifica si una acción fue presionada este frame."""
        self._mapper.assert_action(context, action)
        return self._actions.is_pressed((context, action))
    
    def is_action_held(self, context: str, action: str, window: int = 10) -> bool:
        """Verifica si una acción está siendo mantenida."""
        self._mapper.assert_action(context, action)
        return self._actions.is_held((context, action), window)
    
    def is_action_released(self, context: str, action: str) -> bool:
        """Verifica si una acción fue liberada este frame."""
        self._mapper.assert_action(context, action)
        return self._actions.is_released((context, action))
    
    # --- API de mouse ---
    @property
    def mouse_pos(self) -> tuple[int, int]:
        """Obtiene la posición actual del mouse."""
        return pygame.mouse.get_pos()  
    
    def is_mouse_pressed(self, button: str) -> bool:
        """Verifica si un botón del mouse fue presionado."""
        return self._mouse.is_pressed(MouseButton.from_name(button))
    
    def is_mouse_held(self, button: str, window: int = 10) -> bool:
        """Verifica si un botón del mouse está siendo mantenido."""
        return self._mouse.is_held(MouseButton.from_name(button), window)
    
    def is_mouse_released(self, button: str) -> bool:
        """Verifica si un botón del mouse fue liberado."""
        return self._mouse.is_released(MouseButton.from_name(button))
    
    def is_mouse_in_rect(self, rect: pygame.Rect) -> bool:
        """Verifica si el mouse está dentro de un rectángulo."""
        return rect.collidepoint(self.mouse_pos)
    
    def is_mouse_pressed_in_rect(self, button: str, rect: pygame.Rect) -> bool:
        """Verifica si un botón fue presionado dentro de un rectángulo."""
        return self.is_mouse_pressed(button) and self.is_mouse_in_rect(rect)
    
    def is_mouse_held_in_rect(self, button: str, rect: pygame.Rect, window: int = 10) -> bool:
        """Verifica si un botón está siendo mantenido dentro de un rectángulo."""
        return self._mouse.is_held(MouseButton.from_name(button), window) and self.is_mouse_in_rect(rect)

    def is_released_in_rect(self, button: str, rect: pygame.Rect) -> bool:
        """Verifica si un botón ha sido liberado dentro de un rectángulo."""
        return self._mouse.is_released(MouseButton.from_name(button)) and self.is_mouse_in_rect(rect)

    # --- API de teclas físicas (opcional, para debug) ---
    def is_key_pressed(self, pygame_key: int) -> bool:
        """Verifica si una tecla física fue presionada."""
        return self._keys.is_pressed(pygame_key)
    
    def is_key_held(self, pygame_key: int, window: int = 10) -> bool:
        """Verifica si una tecla física está siendo mantenida."""
        return self._keys.is_held(pygame_key, window)
    
    def is_key_released(self, pygame_key: int) -> bool:
        """Verifica si una tecla física fue liberada este frame."""
        return self._keys.is_released(pygame_key)