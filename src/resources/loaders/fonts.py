from typing import TYPE_CHECKING
from src.util.paths import get_asset

if TYPE_CHECKING:
        from src.resources.resource_manager import ResourceManager

def _load_fonts(rm: "ResourceManager") -> None:
        different_sizes = {48, 90, 100, 150}
        rm.load_font("Estandar", str(get_asset("fonts", "04B03.ttf")), different_sizes)