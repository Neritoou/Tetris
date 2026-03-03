import pygame
from typing import Optional, Callable, TYPE_CHECKING

from src.ui import UIElement

if TYPE_CHECKING:
    from components import UILabel

class UIButton(UIElement):
    """
    Un botón interactivo que admite estados visuales y ejecución de funciones.
    
    Gestiona tres estados visuales (normal, hover y presionado) mediante el cambio
    de superficies (Surfaces). Puede contener un UILabel interno que se centra
    automáticamente y sincroniza su visibilidad y transparencia con el botón.
    """
    def __init__(
            self, name: str, x: int, y: int, callback_function: Callable[[], None],
            base_button: pygame.Surface, hover_button: Optional[pygame.Surface] = None,
            press_button: Optional[pygame.Surface] = None, *,
            text: Optional["UILabel"] = None, visible: bool = True, enabled: bool = True
    ):
        """
        Inicializa las propiedades de un botón.
        
        Args:
            callback_function: Función que se ejecuta al activar el botón.
            base_button: Imagen del botón en estado normal.
            hover_button: Imagen del botón al pasar el mouse por encima.
            press_button: Imagen del botón al hacer click.   
            text: Etiqueta de texto contenida en el botón.
        """
        # Estados del botón (normal, hover, press)
        self.button_surface = base_button
        self.hover_surface = hover_button if hover_button else base_button
        self.press_surface = press_button if press_button else base_button

        self._surface = base_button
        self._function = callback_function
        self._text = text

        width, height = self.button_surface.get_size()

        if self._text:
            self._center_text_on_button()

        # Estados de interacción
        self._is_hovered: bool = False
        self._is_pressed: bool = False

        super().__init__(name, x, y, width, height, visible=visible, enabled=enabled)

        if self._text:
            self._center_text_on_button()


    # --- PROPIEDADES PARA ACTUALIZAR EL ESTADO ---
    @property
    def is_hovered(self) -> bool:
        """Permite a otros objetos leer si el mouse esta encima."""
        return self._is_hovered
    
    @is_hovered.setter
    def is_hovered(self, value: bool) -> None:
        self._is_hovered = value

    @property
    def is_pressed(self) -> bool:
        """Permite a otros objetos saber si el botón está presionado."""
        return self._is_pressed

    @is_pressed.setter
    def is_pressed(self, value: bool) -> None:
        self._is_pressed = value

    def set_enabled(self, status: bool) -> None:
        """Activa o desactiva el botón y visualmente le da un tono grisáceo."""
        self.enabled = status
        
        if not status:
            self.alpha = 128  # Semitransparente
            self._is_hovered = False
            self._is_pressed = False
        else:
            self.alpha = 255

    def set_text(self, new_text: str) -> None:
        """Actualiza el texto del botón de ser necesario."""
        if self._text:
            self._text.set_text(new_text)
            self._center_text_on_button()

    # --- MÉTODOS ABSTRACTOS DE UIElement ---
    def update(self, dt: float) -> None:
        super().update(dt)

        if self.is_pressed and self.press_surface:
            self._surface = self.press_surface
        elif self.is_hovered and self.hover_surface:
            self._surface = self.hover_surface
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
        if self.enabled and self._function:
            self._function()

    def _center_text_on_button(self) -> None:
        """Centra el texto sobre el botón."""
        if self._text:
            self._text.rect.center = self.rect.center