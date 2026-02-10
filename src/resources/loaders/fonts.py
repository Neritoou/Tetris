from typing import TYPE_CHECKING

if TYPE_CHECKING:
        from ..resource_manager import ResourceManager

def _load_fonts(rm: "ResourceManager") -> None:
        different_sizes = {48, 90, 100, 150}
        rm.load_font("Estandar", "assets/fonts/04B03.ttf", different_sizes)