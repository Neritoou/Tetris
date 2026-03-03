import pygame
from typing import TYPE_CHECKING

from src.ui import UIElement

if TYPE_CHECKING:
    from src.ui import ColorValue

class UILabel(UIElement):
    """Representa una etiqueta de texto en la interfaz de usuario."""
    def __init__(
            self, name: str, x: int, y: int,
            text: str, font: pygame.font.Font,
            color: "ColorValue" = (255, 255, 255), *, center: bool = True,
            visible: bool = True, alpha: int = 255, scale: float = 1.0,
            angle: int = 0
            ):
        """
        Inicializa las propiedades de las etiquetas.
        
        Args:
            text: Texto de la etiqueta.
            font: Fuente del texto.
            color: Color del texto.
        """
        # Datos del texto
        self.font = font
        self.text = text
        self.color = pygame.Color(color)
        self._last_alpha: int = -1  # fuerza el set en el primer frame
        self._is_centered = center

        # Superficie inicial
        self.text_surface = font.render(self.text, True, self.color)
        width, height = self.text_surface.get_size()

        super().__init__(name, x, y, width, height, visible=visible, alpha=alpha, scale=scale, angle=angle)
        
        if self._is_centered:
            self.center_at(x)

    def set_text(self, new_text: str) -> None:
        """Actualiza el contenido del texto y ajusta el área de colisión."""
        if self.text != new_text:
            self.text = new_text
            self.text_surface = self.font.render(self.text, True, self.color)
            
            self._update_rect(self.text_surface)

    def set_color(self, new_color: "ColorValue") -> None:
        """Cambia el color del texto y regenera la superficie."""
        temp_color = pygame.Color(new_color)

        if self.color != temp_color:
            self.color = temp_color
            self.text_surface = self.font.render(self.text, True, self.color)

    def set_font(self, new_font: pygame.font.Font) -> None:
        """Cambia la fuente del texto y recalcula el tamaño del Rect."""
        self.font = new_font
        self.text_surface = self.font.render(self.text, True, self.color)

        self._update_rect(self.text_surface)

    def center_at(self, x: int) -> None:
        """Posiciona el texto centrándolo horizontalmente."""
        self.rect.centerx = x

    def _update_rect(self, text_surface: pygame.Surface) -> None:
        """
        Recalcula y actualiza el área (Rect) de la etiqueta basándose en una nueva superficie.
        
        Mantiene la posición actual del texto, respetando si fue configurado
        para estar centrado (centerx) o anclado a la izquierda (topleft).

        Args:
            text_surface: La nueva superficie de Pygame generada con el texto actualizado.
        """
        if self._is_centered:
            cx = self.rect.centerx
            self.rect = text_surface.get_rect(centerx=cx, y=self.rect.y)
        else:
            pos = self.rect.topleft
            self.rect = text_surface.get_rect(topleft=pos)

    # --- MÉTODOS ABSTRACTOS DE UIElement ---
    def render(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return

        current = int(self.alpha)
        if current != self._last_alpha:
            self.text_surface.set_alpha(current)
            self._last_alpha = current

        surface.blit(self.text_surface, self.rect)

    def update(self, dt: float) -> None:
        super().update(dt)