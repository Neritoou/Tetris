import pygame
from typing import TYPE_CHECKING

from src.ui import UIElement

if TYPE_CHECKING:
    from src.ui import ColorValue

class UIPanel(UIElement):
    """Un panel estático con fondo translúcido y bordes redondeados."""
    def __init__(
            self, name: str, x: int, y: int, width: int, height: int,
            bg_color: "ColorValue", border_color: "ColorValue", border_width: int = 2, radius: int = 16,
            visible: bool = True, alpha: int = 255
    ):
        super().__init__(name, x, y, width, height, visible=visible, alpha=alpha)
        
        self.bg_color = bg_color
        self.border_color = border_color
        self.border_width = border_width
        self.radius = radius

        # Renderizamos la superficie base una sola vez
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self._draw_panel()

    def _draw_panel(self):
        self.image.fill((0, 0, 0, 0))
        pygame.draw.rect(self.image, self.bg_color, self.image.get_rect(), border_radius=self.radius)
        pygame.draw.rect(self.image, self.border_color, self.image.get_rect(), width=self.border_width, border_radius=self.radius)

    def render(self, surface: pygame.Surface) -> None:
        if not self.visible:
            return
        self.image.set_alpha(int(self.alpha))
        surface.blit(self.image, self.rect)

    def update(self, dt: float) -> None:
        super().update(dt)