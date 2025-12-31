from ...constants import PIECE_DEFINITIONS, BLOCK_W, BLOCK_H, BLOCK_PW, BLOCK_PH
from typing import TYPE_CHECKING

if TYPE_CHECKING:
        from ..resource_manager import ResourceManager
        
def _load_spritesheets(rm: "ResourceManager") -> None:
        # BLOQUES PARA LAS PIEZAS
        rm.load_spritesheet("BlocksType", "assets/spritesheets/tetromino.png", (BLOCK_W,BLOCK_H), (BLOCK_PW,BLOCK_PH))
