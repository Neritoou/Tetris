from ...constants import PIECE_DEFINITIONS
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..piece_library import PieceSurfaces
    from ..resource_manager import ResourceManager
    
def _load_pieces(rm: "ResourceManager") -> None:
    """Registra las piezas del Tetris usando la constante PIECE_DEFINITIONS."""
    sheet = rm.get_spritesheet("BlocksType") 

    # Se itera en la Constante para obtener los datos de la Pieza
    for name, info in PIECE_DEFINITIONS.items():
        col = info["spritesheet_col"] 
        base_matrix = info["matrix"]

        # Se obtiene directamente las Surfaces de los Bloques para la Pieza
        frames = sheet.get_frames_at_col(col) 
        # Se asignan a su respectivo diccionario
        blocks: PieceSurfaces = {
            "normal": frames[0],
            "placed": frames[1],
            "ghost": frames[2]
        }
        rm.load_piece(name, base_matrix, blocks)