from typing import Dict, List, Set, Tuple
import pygame
from .map_config import KeyMapConfig

class KeyInputManager:
    def __init__(self) -> None:
        # Estados de teclas
        self._pressed: Set[Tuple[str, str]] = set()
        self._held: Set[Tuple[str, str]] = set()
        self._released: Set[Tuple[str, str]] = set()

        # Mapeo inverso: tecla pygame -> lista de (context, action)
        self._key_to_actions: Dict[int, List[Tuple[str, str]]] = KeyMapConfig.get_key_to_actions()


    @property
    def pressed(self) -> Set[Tuple[str, str]]:
        return self._pressed
    
    @property
    def help(self) -> Set[Tuple[str, str]]:
        return self._held
    
    @property
    def released(self) -> Set[Tuple[str, str]]:
        return self._released
    
    def is_pressed(self, context: str, action: str) -> bool:
        """Verifica si la acción está presionada en el contexto."""
        KeyMapConfig.assert_action(context, action)
        return (context, action) in self._pressed

    def is_held(self, context: str, action: str) -> bool:
        """Verifica si la acción está mantenida en el contexto."""
        KeyMapConfig.assert_action(context, action)
        return (context, action) in self._held

    def is_released(self, context: str, action: str) -> bool:
        """Verifica si la acción ha sido liberada en el contexto."""
        KeyMapConfig.assert_action(context, action)
        return (context, action) in self._released
    
    # Detectar input del Teclado
    def _handle_event(self, event: pygame.event.Event) -> None:
        """Maneja los eventos de teclas (KEYDOWN, KEYUP)."""
        key = event.key
        # Se obtienen todas las acciones relacionadas a la key
        actions = self._key_to_actions.get(key, [])
                
        for context, action in actions:
            identifier = (context, action)

            if event.type == pygame.KEYDOWN:
                # Si es la primera vez que se presiona, añadir a _pressed
                if identifier not in self._held:
                    self._pressed.add(identifier)  
                self._held.add(identifier) # Siempre se marca como "held"
                    
            elif event.type == pygame.KEYUP:
                self._released.add(identifier)  # Marcar como liberado
                self._held.discard(identifier)  # Eliminar de los mantenidos   
