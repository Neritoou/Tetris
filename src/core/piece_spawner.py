from typing import Dict, TYPE_CHECKING
from .piece import Piece

if TYPE_CHECKING:
    from .piece_bag import PieceBag
    from .types import PieceData

# (!) Ver si se elimina
class PieceSpawner:
    def __init__(self, bag: "PieceBag", pieces: "Dict[str, PieceData]"):
        self.bag = bag
        self.pieces = pieces

    def new_piece(self) -> Piece:
        """Genera una nueva pieza desde la bolsa."""
        piece_name = self.bag.get_next_piece()
        piece_data = self.pieces[piece_name]
        new_piece = Piece(piece_name, piece_data)
        return new_piece