from typing import TYPE_CHECKING
from ...util import get_asset

if TYPE_CHECKING:
    from ..resource_manager import ResourceManager

def _load_images(rm: "ResourceManager") -> None:
        # BOARD BASE
        rm.load_image("Board",str(get_asset("images","grid.png")))