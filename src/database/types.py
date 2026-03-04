from dataclasses import dataclass
from enum import Enum


class RulesetName(str, Enum):
    GUIDELINE = "guideline"
    NES       = "nes"


@dataclass
class Record:
    """
    Representa un run completado de una partida de Tetris.

    Attributes:
        score:    Puntaje final obtenido.
        lines:    Total de líneas eliminadas.
        level:    Nivel alcanzado al finalizar.
        tetrises: Cantidad de limpiezas de 4 líneas.
        date:     Fecha del run en formato ISO (YYYY-MM-DD).
    """
    score:    int
    lines:    int
    level:    int
    tetrises: int
    date:     str


@dataclass
class RulesetRecords:
    """
    Almacena el top de records de un ruleset específico.

    Attributes:
        name:    Nombre del ruleset.
        records: Lista de records ordenados por score DESC.
    """
    name:    RulesetName
    records: list[Record]

    @property
    def top_record(self) -> Record | None:
        """Retorna el mejor record o None si no hay ninguno."""
        return self.records[0] if self.records else None