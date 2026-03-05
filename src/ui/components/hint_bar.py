import pygame
from src.ui.ui_element import UIElement

_COLOR_KEY  = (190, 190, 190)
_COLOR_DESC = (130, 130, 130)
_GAP        = 30
_INNER_GAP  = 6


class UIHintBar(UIElement):
    """
    Barra de hints pre-renderizada. Cero costo en render().

    El posicionamiento usa los anchor points nativos de pygame.Rect:
        HintBar(..., midbottom=(w // 2, h - 20))
        HintBar(..., midtop=(w // 2, 20))
        HintBar(..., center=(w // 2, h // 2))
        HintBar(..., topleft=(650, 520))

    Hints Ejemplo:
        HintBar("hints", font, [
            ("CONFIRM, "confirm"), "Confirmar"),
            ("Esc", "Volver"),
        ], midbottom=(w // 2, h - 20))
    """

    def __init__(
        self,
        element_id: str,
        font: pygame.font.Font,
        hints: list[tuple[str, str]],
        *,
        color_key:  tuple[int, int, int] = _COLOR_KEY,
        color_desc: tuple[int, int, int] = _COLOR_DESC,
        gap:        int = _GAP,
        inner_gap:  int = _INNER_GAP,
        **anchor,
    ):
        pieces: list[tuple[pygame.Surface, pygame.Surface]] = [
            (
                font.render(f"[{key}]", True, color_key),
                font.render(desc,       True, color_desc),
            )
            for key, desc in hints
        ]

        total_w = (
            sum(k.get_width() + inner_gap + d.get_width() for k, d in pieces)
            + gap * (len(pieces) - 1)
        )
        total_h = max(
            max(k.get_height(), d.get_height()) for k, d in pieces
        )

        surf = pygame.Surface((total_w, total_h), pygame.SRCALPHA)
        cur_x = 0
        for k_surf, d_surf in pieces:
            surf.blit(k_surf, (cur_x, 0))
            cur_x += k_surf.get_width() + inner_gap
            surf.blit(d_surf, (cur_x, 0))
            cur_x += d_surf.get_width() + gap

        rect = surf.get_rect(**anchor)

        super().__init__(element_id, rect.x, rect.y, total_w, total_h, visible=True)

        self._surf = surf

    def update(self, dt: float) -> None:
        pass

    def render(self, surface: pygame.Surface) -> None:
        surface.blit(self._surf, self.rect.topleft)