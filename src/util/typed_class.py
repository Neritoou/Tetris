from pygame import Surface
from typing import List, TypedDict
from numpy import ndarray

class PieceSurfaces(TypedDict):
    normal: Surface
    placed: Surface
    ghost: Surface


class PieceData(TypedDict):
    matrices: List[ndarray]
    surfaces: PieceSurfaces