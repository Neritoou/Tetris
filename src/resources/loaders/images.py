from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..resource_manager import ResourceManager

def _load_images(rm: "ResourceManager") -> None:
        # BOARD BASE
        rm.load_image("Board","assets/images/grid.png")