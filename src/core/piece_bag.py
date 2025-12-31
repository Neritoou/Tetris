import random
from typing import List

from ..constants import PIECE_DEFINITIONS

class PieceBag:
    """
    Gestiona la generación de piezas utilizando un sistema de bolsa (Bag System).

    Garantiza una distribución equitativa de los tetrominos, evitando rachas 
    largas de la misma pieza o la ausencia prolongada de una específica. 
    
    Funciona llenando una 'bolsa' con un set completo de piezas, barajándolas y 
    entregándolas una a una.
    """
    def __init__(self, bag_size: int = 7) -> None:
        """
        Inicializa la bolsa de piezas del juego.

        Args:
            bag_size: Tamaño de la bolsa.
        """
        # Extrae las llaves del diccionario de PIECE_DEFINITIONS ("O", "T", etc.)
        self.available_pieces = list(PIECE_DEFINITIONS.keys())
        
        # Verifica que el tamaño sea adecuado
        self.__verify_bag_size(bag_size)
        self.bag_size = bag_size
        
        self.queue: List[str] = []
        self.__fill_bag()

    def __str__(self) -> str:
        return f"A la bolsa de piezas le quedan {len(self.queue)} piezas, y la proxima pieza es {self.queue[0] if self.queue else 'None'}."

    def get_next_piece(self) -> str:
        """
        Extrae y devuelve el identificador de la siguiente pieza en la cola.
        Si la bolsa se vacía, se rellena automáticamente.
        
        Returns:
            str: El nombre de la pieza (p. ej., 'I', 'J', 'O').
        """
        if not self.queue:
            self.__fill_bag()
        return self.queue.pop(0)
    
    def peek_next(self, count: int) -> List[str]:
        """
        Permite previsualizar las próximas piezas sin sacarlas de la cola.
        
        Args:
            count: Cantidad de piezas que se desean observar.

        Returns:
            List[str]: Lista con los nombres de las próximas n piezas.
        """
        # Si no se tienen suficientes piezas para mostrar, se rellena la bolsa
        while len(self.queue) < count:
            self.__fill_bag()

        return self.queue[:count]
    
    # --- MÉTODOS PRIVADOS ---
    def __verify_bag_size(self, bag_size: int) -> None:
        """
        Valida que el tamaño de la bolsa sea un múltiplo exacto del set de piezas.
        Con el fin de asegurar que todas las piezas tenga la misma probabilidad de
        aparición en cada ciclo de llenado.

        Raises:
            ValueError: Si bag_size es 0 o no es divisible por el número de piezas disponibles.
        """
        num_tetrominos = len(self.available_pieces)     # Calcula la cantidad de piezas disponibles

        # Lanza un error si el tamaño de la bolsa (bag_size) no es adecuado
        if bag_size % num_tetrominos != 0 or bag_size == 0:
            raise ValueError(f"El tamaño de la bolsa ({bag_size}) debe ser múltiplo de {num_tetrominos}.")
    
    def __fill_bag(self) -> None:
        """Genera un nuevo lote de piezas, lo baraja y lo añade a la cola."""
        new_batch = []

        # Calcula la cantidad de copias que debe tener cada pieza
        num_copies = self.bag_size // len(self.available_pieces)

        for piece in self.available_pieces:
            new_batch.extend([piece] * num_copies)

        random.shuffle(new_batch)           # Baraja las piezas
        self.queue.extend(new_batch)        # Agrega las piezas a la bolsa