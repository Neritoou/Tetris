import pygame
from typing import Optional, Callable, TYPE_CHECKING

from src.ui import UIElement

if TYPE_CHECKING:
    from src.ui.components import UILabel

class UIButton(UIElement):
    """
    Un botón interactivo que admite estados visuales y ejecución de funciones.
    Puede contener un UILabel interno que se centra automáticamente.
    """
    def __init__(
            self, name: str, x: int, y: int, callback_function: Callable[[], None],
            base_button: pygame.Surface, selected_button: pygame.Surface,
            *, text: Optional["UILabel"] = None, text_y: int = 0,
            visible: bool = True, alpha: int = 255
    ):
        """
        Inicializa las propiedades de un botón.
        
        Args:
            callback_function: Función que se ejecuta al activar el botón.
            base_button: Imagen del botón en estado normal.
            selected_button: Imagen del botón seleccionado.
            text: Etiqueta de texto contenida en el botón.
        """
        # Estados del botón (normal y selected)
        self.button_surface = base_button
        self.selected_surface = selected_button

        width, height = self.button_surface.get_size()

        super().__init__(name, x, y, width, height, visible=visible, alpha=alpha)

        self._surface = base_button
        self._function = callback_function
        self._text = text

        self._is_selected: bool = False
        
        self.text_y = text_y
        
        if text_y == 0:
            self._center_text_on_button()
        else:
            self._pos_text(text_y)



    # --- PROPIEDADES PARA ACTUALIZAR EL ESTADO ---
    @property
    def is_selected(self) -> bool:
        """Permite a otros objetos leer si el mouse esta encima."""
        return self._is_selected
    
    @is_selected.setter
    def is_selected(self, value: bool) -> None:
        self._is_selected = value

    def set_text(self, new_text: str) -> None:
        """Actualiza el texto del botón de ser necesario."""
        if self._text:
            self._text.set_text(new_text)

            if self._text and self.text_y == 0:
                self._center_text_on_button()
            else:
                self._pos_text(self.text_y)



    # --- MÉTODOS ABSTRACTOS DE UIElement ---
    def update(self, dt: float) -> None:
        super().update(dt)

        if self.is_selected:
            self._surface = self.selected_surface
        else:
            self._surface = self.button_surface

        if self._text:
            self._text.alpha = self.alpha
            self._text.visible = self.visible
            self._text.update(dt)
    
    def render(self, surface: pygame.Surface):
        if not self.visible:
            return
        
        self._surface.set_alpha(int(self.alpha))
        surface.blit(self._surface, self.rect)

        if self._text:
            self._text.render(surface)



    # --- MÉTODOS PRIVADOS ---
    def on_click(self) -> None:
        """Ejecuta la función callback cuando el botón es presionado."""
        if self._function:
            self._function()

    def _center_text_on_button(self) -> None:
        """Centra el texto sobre el botón."""
        if self._text:
            self._text.rect.center = self.rect.center

    def _pos_text(self, y: int = 10) -> None:
        if self._text:
            self._text.rect.centerx = self.rect.centerx
            self._text.rect.y = self.rect.y + y