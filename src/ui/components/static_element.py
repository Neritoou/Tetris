import pygame
from src.ui import UIElement

class UIStatic(UIElement):
    """
    Elemento visual estático sin interacción para la inferfaz de usuario.

    Se utiliza para renderizar imágenes que no requieren interacción,
    como fondos, iconos, marcos o elementos decorativos del HUD que no
    responden a eventos del mouse.
    """
    def __init__(
            self, name: str, x: int, y: int,
            image: pygame.Surface, *, visible: bool = True,
            alpha: int = 255, scale: float = 1.0, angle: int = 0
    ):
        """
        Inicializa las propiedades de los elementos estáticos.
        
        Args:
            image: La superficie de la imagen que se mostrará.
        """
        self.original_img = image
        self.img = self._apply_transformations(image, scale, angle)
        
        width, height = self.img.get_size()

        super().__init__(name, x, y, width, height, visible=visible,
                         alpha=alpha, scale=scale, angle=angle)



    # --- MÉTODOS ABSTRACTOS DE UIElement ---
    def render(self, surface: pygame.Surface) -> None:
        """Renderiza el elemento en la superficie destino."""
        if not self.visible:
            return
        
        self.img.set_alpha(int(self.alpha))
        surface.blit(self.img, self.rect)

    def update(self, dt: float) -> None:
        super().update(dt)



    # --- MÉTODOS PRIVADOS ---
    def _apply_transformations(self, img: pygame.Surface, scale: float, angle: int) -> pygame.Surface:
        """Aplica transformaciones a la imagen (escala o rotación)."""        
        new_img = img

        if scale != 1.0:
            width, height = img.get_size()
            new_img = pygame.transform.scale(new_img, (int(width * scale), int(height * scale)))
        if angle != 0:
            new_img = pygame.transform.rotate(new_img, angle)
        return new_img