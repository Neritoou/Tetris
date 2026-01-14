from typing import List, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
    from .piece_bag import PieceBag
    from .types import PieceDataType, PiecesPreviewType
    from pygame import Surface

class PiecesPreview:
    def __init__(self, data: "PieceDataType", bag: "PieceBag", *, preview: "PiecesPreviewType"):
        """
        args:
        - data: dict[str, PieceData] con info de piezas y sus surfaces
        - bag: instancia de PieceBag
        - preview: PiecePreviewConfig con la info: pos_x, pos_y: coordenadas donde se dibuja la primera pieza,
            max_width: ancho máximo de la zona de preview (para centrar las piezas horizontalmente), margin: espacio
            vertical entre piezas y preview_count: cuántas piezas mostrar
        """
        self._data = data
        self._bag = bag
        self._pos_x = preview["pos_x"]
        self._pos_y = preview["pos_y"]
        self._max_width = preview["max_width"]
        self._margin = preview["margin"]

        # Cache de posiciones X (centrado de las piezas en el eje X)
        self._x_cache = {name: self._pos_x + (self._max_width - data[name]["surfaces"]["normal"].get_width()) // 2
                         for name in data}

        # Lista de tuplas (surface, x, y)
        self._preview_list: "List[Tuple[Surface, int, int]]" = []
        # Cuantas Piezas mostrar
        self.count = preview["preview_count"]
        # Generar la vista previa inicial
        self.generate()

    def generate(self):
        """Genera la lista inicial de previews"""
        piece_names = self._bag.peek_next(self.count)  # Obtén las primeras preview_count piezas
        self._preview_list = []
        y = self._pos_y # Posición vertical inicial
        # Calcular la altura de cada pieza dinámicamente
        for name in piece_names:
            surface = self._data[name]["surfaces"]["normal"]
            x = self._x_cache[name]

            # Añadir la pieza con la posición correcta
            self._preview_list.append((surface, x, y))
            # Acumular altura para la siguiente pieza
            y += surface.get_height() + self._margin 
            
    def get(self) -> "List[Tuple[Surface, int, int]]":
        """Devuelve la lista de previsualización (surface, x, y)"""
        return self._preview_list
