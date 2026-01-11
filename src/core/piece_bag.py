import random
from typing import List

class PieceBag:
    """
    Gestiona la generación de piezas utilizando un sistema de bolsa (Bag System).

    Garantiza una distribución equitativa de los tetrominos, evitando rachas 
    largas de la misma pieza o la ausencia prolongada de una específica. 
    
    Funciona llenando una 'bolsa' con un set completo de piezas, barajándolas y 
    entregándolas una a una.
    """
    def __init__(self, pieces: dict, multiplier: int) -> None:
        """
        Inicializa la bolsa de piezas del juego.

        Args:
           multiplier (int): Cantidad de veces que se agrega el set completo piezas a la bolsa antes de mezclar.
        """
        # Extrae las llaves del diccionario de PIECE_DEFINITIONS ("O", "T", etc.)
        self.available_pieces: list[str] = list(pieces.keys())
        self.__valid_multiplier(multiplier)
        self.multiplier = multiplier
        
        self.queue: List[str] = []
        self.__fill_bag()

    def get_next_piece(self) -> str:
        """
        Extrae y devuelve el identificador de la siguiente pieza en la cola.

        Si la bolsa se vacía, se rellena automáticamente.
        Returns:
            str: El nombre de la pieza (p. ej., 'I', 'J', 'O').
        """
        if not self.queue: self.__fill_bag()
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
    
    # --- HELPERS ---
    def __fill_bag(self) -> None:
        """Genera un nuevo lote de piezas, lo baraja y lo añade a la cola."""
        new_batch = self.available_pieces * self.multiplier
        random.shuffle(new_batch) # Baraja las piezas
        self.queue.extend(new_batch) # Agrega las piezas a la bolsa

    def __valid_multiplier(self, multiplier: int) -> None:
        if multiplier <= 0:
            raise ValueError(
                f"PieceBag: multiplicador inválido ({multiplier}). "
                "Debe ser un entero positivo mayor que cero."
            )
            
    def __str__(self) -> str:
        return f"A la bolsa de piezas le quedan {len(self.queue)} piezas, y la proxima pieza es {self.queue[0] if self.queue else 'None'}."