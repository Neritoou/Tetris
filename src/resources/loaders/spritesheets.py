from ...constants import BLOCK_W, BLOCK_H, BLOCK_PW, BLOCK_PH
from typing import TYPE_CHECKING
from ...util import get_asset

if TYPE_CHECKING:
        from ..resource_manager import ResourceManager
        
def _load_spritesheets(rm: "ResourceManager") -> None:
        # BLOQUES PARA LAS PIEZAS
        rm.load_spritesheet("BlocksType", str(get_asset("spritesheets","tetromino.png")), (BLOCK_W,BLOCK_H), (BLOCK_PW,BLOCK_PH))
