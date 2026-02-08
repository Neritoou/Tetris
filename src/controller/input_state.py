from typing import Generic, TypeVar

T = TypeVar('T')

class InputState(Generic[T]):
    """
    Estado genérico de inputs (teclas, botones de mouse, etc).
    
    Maneja el ciclo de vida: pressed → held → released
    """
    def __init__(self):
        self._pressed: set[T] = set()            # Inputs presionados este frame
        self._held: set[T] = set()               # Inputs actualmente mantenidos
        self._released: set[T] = set()           # Inputs liberados este frame
        self._frames_pressed: dict[T, int] = {}  # Contador de frames presionados porcada input
    
    @property
    def pressed(self) -> set[T]:
        """Inputs que fueron presionados este frame."""
        return self._pressed
    
    @property
    def held(self) -> set[T]:
        """Inputs que están siendo mantenidos."""
        return self._held
    
    @property
    def released(self) -> set[T]:
        """Inputs que fueron liberados este frame."""
        return self._released
    
    def is_pressed(self, item: T) -> bool:
        """Verifica si el input fue presionado este frame."""
        return item in self._pressed
    
    def is_held(self, item: T, window: int) -> bool:
        """
        Detecta si el input está siendo mantenido más allá de la ventana de frames.
        `window` define cuántos frames deben pasar para considerarlo 'held'.
        """        
        return self._frames_pressed.get(item, 0) > window
    
    def is_released(self, item: T) -> bool:
        """Verifica si el input fue liberado este frame."""
        return item in self._released
    
    def clear_frame_state(self) -> None:
        """
        Limpia los estados transitorios de pressed y released
        y actualiza los contadores de frames de los inputs mantenidos.
        """
        self._pressed.clear()
        self._released.clear()
        
        # Incrementar contador de frames para held
        for item in self._frames_pressed:
            self._frames_pressed[item] += 1
    
    def handle_down(self, item: T) -> None:
        """Maneja cuando un input es presionado."""
        if item in self._frames_pressed:
            self._frames_pressed[item] += 1
        else:
            self._pressed.add(item)         
            self._frames_pressed[item] = 1

        self._held.add(item)
    
    def handle_up(self, item: T) -> None:
        """Maneja cuando un input es liberado."""
        self._released.add(item)
        self._held.discard(item)
        self._frames_pressed.pop(item, None)
