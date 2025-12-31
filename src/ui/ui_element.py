from abc import ABC, abstractmethod
import pygame
from typing import Tuple

class UIElement(ABC):
    """Clase base abstracta para todos los elementos de la interfaz de usuario."""
    def __init__(self, name: str,
        surface: pygame.Surface, position: Tuple[int, int], *,
        copy_surface: bool = False, scale: float = 1.0,
        visible: bool = True, enabled: bool = True,
    ):
        """
        Inicializa las propiedades comunes de los elementos UI.
        
        Args:
            name (str): El nombre del elemento UI.
            surface (pygame.Surface): La superficie del recurso gráfico del elemento.
            position (Tuple[int, int]): La posición en la pantalla (x, y).
            copy_surface (bool): Si True, se hará una copia de la superficie para no compartirla con otros elementos.
            scale (float): Factor de escala para el tamaño del elemento.
            visible (bool): Si el elemento es visible en pantalla.
            enabled (bool): Si el elemento está habilitado para interacción.
        """
        self._name: str = name
        self._base_surface: pygame.Surface = surface
        self._scale: float = scale
        self._surface: pygame.Surface = self.__build_surface(copy_surface)
        self._rect: pygame.Rect = self._surface.get_rect(topleft=position)

        self._surf_copied: bool = copy_surface
        self._visible: bool = visible
        self._enabled: bool = enabled

    @property
    def position(self) -> Tuple[int, int]:
        """Obtiene la posición del elemento UI (esquinas superiores izquierda)."""
        return self._rect.topleft

    @property
    def scale(self) -> float:
        """Obtiene el factor de escala actual del elemento."""
        return self._scale
    
    def is_visible(self) -> bool:
        """Devuelve si el elemento es visible."""
        return self._visible
    
    def is_enabled(self) -> bool:
        """Devuelve si el elemento está habilitado para la interacción."""
        return self._enabled

    def set_visible(self, visible: bool) -> None:
        """Actualiza la visibilidad del elemento UI."""
        self._visible = visible

    def set_enabled(self, enabled: bool) -> None:
        """Actualiza si el elemento está habilitado para la interacción."""
        self._enabled = enabled

    def set_position(self, position: Tuple[int, int]) -> None:
        """Actualiza la posición del elemento UI en la pantalla."""
        self._rect.topleft = position

    def set_scale(self, scale: float) -> None:
        """
        Actualiza la escala de la surface y ajusta el rect en consecuencia.
        
        Si el elemento no fue copiado, no se puede cambiar la escala.

        Args:
            scale (float): El factor de escala.
            
        Raises:
            ValueError: Si se intenta cambiar la escala de un elemento no copiado o si la escala es negativa.
        """
        if not self._surf_copied:
            raise ValueError(f"UI Element: '{self._name}' no se puede cambiar la escala de un elemento no copiado. "
                            f"El elemento es único y su tamaño no debe modificarse. "
                            f"Habilita la copia del recurso si es necesario cambiar la escala.")

        if scale < 0:
            raise ValueError(f"UI Element: '{self._name}' no puede ser escalado negativamente '{scale}'")
        
        if scale == self._scale:
            return  
    
        old_position = self._rect.topleft 
        self._scale = scale
        self._surface = self.__build_surface(copy_surface=True)
        
        # Se Actualiza el tamaño del rect para que coincida con la nueva surface
        self._rect.size = self._surface.get_size()

        # Si la escala no es 1.0, se ajusta la posición para que la relación visual se mantenga
        if self._scale != 1.0:
            self._rect.topleft = old_position # Se coloca el rect en la misma posición


    @abstractmethod
    def render(self, surface: pygame.Surface) -> None:
        pass

    @abstractmethod
    def update(self, dt: float) -> None:
        pass


    # --- HELPERS ---
    def __build_surface(self, copy_surface: bool) -> pygame.Surface:
        """
        Construye la superficie del elemento, utilizando una copia si es necesario,
        y aplicando la escala si no es 1.0.
        """
        surf = self._base_surface.copy() if copy_surface else self._base_surface
        if self._scale != 1.0:
            w, h = surf.get_size()
            surf = pygame.transform.smoothscale(surf, (int(w * self._scale), int(h * self._scale)))
        return surf