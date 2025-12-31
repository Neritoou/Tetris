import pygame
from typing import Tuple
from ..ui_element import UIElement 

class UIStaticElement(UIElement):
    """
    Elemento UI estático.

    Se utiliza para renderizar imágenes que no requieren interacción,
    como fondos, iconos, marcos o elementos decorativos del HUD.
    """
    def __init__(self, name: str,
        surface: pygame.Surface, position: Tuple[int, int], *,
        copy_surface: bool = False, scale: float = 1.0,
        visible: bool = True
    ):
        super().__init__(name, surface, position,
                        copy_surface = copy_surface, scale = scale, 
                        visible = visible, enabled = False)

    def render(self, surface: pygame.Surface) -> None:
        """ Renderiza el elemento en la superficie destino."""
        if not self._visible:
            return
        surface.blit(self._surface, self._rect)

    def update(self, dt: float) -> None:
        """
        Actualiza el estado del elemento.
        UIStaticElement no tiene lógica de actualización, por lo que
        este método se mantiene vacío por diseño.
        """
        pass
