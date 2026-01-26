from typing import Generic, TypeVar, Set

T = TypeVar('T')

class InputState(Generic[T]):
    """
    Estado genérico de inputs (teclas, botones de mouse, etc).
    
    Maneja el ciclo de vida: pressed → held → released
    """
    def __init__(self):
        self._pressed: Set[T] = set()
        self._held: Set[T] = set()
        self._released: Set[T] = set()
    
    @property
    def pressed(self) -> Set[T]:
        """Inputs que fueron presionados este frame."""
        return self._pressed
    
    @property
    def held(self) -> Set[T]:
        """Inputs que están siendo mantenidos."""
        return self._held
    
    @property
    def released(self) -> Set[T]:
        """Inputs que fueron liberados este frame."""
        return self._released
    
    def is_pressed(self, item: T) -> bool:
        """Verifica si el input fue presionado este frame."""
        return item in self._pressed
    
    def is_held(self, item: T) -> bool:
        """Verifica si el input está siendo mantenido."""
        return item in self._held
    
    def is_released(self, item: T) -> bool:
        """Verifica si el input fue liberado este frame."""
        return item in self._released
    
    def clear_frame_state(self) -> None:
        """Limpia los estados transitorios (pressed/released)."""
        self._pressed.clear()
        self._released.clear()
    
    def handle_down(self, item: T) -> None:
        """Maneja cuando un input es presionado."""
        if item not in self._held:
            self._pressed.add(item)
        self._held.add(item)
    
    def handle_up(self, item: T) -> None:
        """Maneja cuando un input es liberado."""
        self._released.add(item)
        self._held.discard(item)