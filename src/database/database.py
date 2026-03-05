import json
from pathlib import Path
from typing import TypedDict
from src.database.types import RulesetName, RulesetRecords, Record
from src.constants import MAX_RECORDS


# Tipos para el JSON crudo
class RawRecord(TypedDict):
    score:    int
    lines:    int
    level:    int
    tetrises: int
    date:     str

class RawDatabase(TypedDict):
    records: dict[str, list[RawRecord]]


class Database:
    """
    Gestiona la persistencia de records del jugador en un archivo JSON.

    Carga el JSON al iniciar y trabaja con los modelos en memoria.
    Cuando hay un cambio relevante serializa todo y sobreescribe el JSON.

    Attributes:
        rulesets: TetrisRecords indexados por RulesetName.
    """

    def __init__(self, path: Path):
        self._path = path
        self.rulesets: dict[RulesetName, RulesetRecords] = {}

    # CARGA Y GUARDADO
    def load(self) -> None:
        """Lee el JSON y construye los modelos en memoria."""
        with self._path.open("r", encoding="utf-8") as f:
            data: RawDatabase = json.load(f)

        self.rulesets = {
            RulesetName(name): self._build_ruleset(RulesetName(name), raw_records)
            for name, raw_records in data["records"].items()
        }

    def save(self) -> None:
        """Serializa los modelos en memoria y sobreescribe el JSON."""
        data: RawDatabase = {
            "records": {
                ruleset.name.value: [self._record_to_dict(r) for r in ruleset.records]
                for ruleset in self.rulesets.values()
            }
        }
        with self._path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    # RECORDS
    def save_record(self, ruleset_name: RulesetName | str, record: Record) -> bool:
        if isinstance(ruleset_name, str):
            ruleset_name = RulesetName(ruleset_name)
        """
        Intenta guardar un record en el top de un ruleset.

        Ordena por score DESC, con lines como desempate.
        Si el record nuevo supera al peor del top lo reemplaza.

        Returns:
            True si el record entró al top, False si no.
        """
        if ruleset_name not in self.rulesets:
            raise ValueError(f"Database: ruleset '{ruleset_name}' no encontrado.")

        records = self.rulesets[ruleset_name].records
        records.sort(key=lambda r: (r.score, r.lines), reverse=True)

        entered = False

        if len(records) < MAX_RECORDS:
            records.append(record)
            records.sort(key=lambda r: (r.score, r.lines), reverse=True)
            entered = True

        elif self._is_better(record, records[-1]):
            records[-1] = record
            records.sort(key=lambda r: (r.score, r.lines), reverse=True)
            entered = True

        if entered:
            self.save()

        return entered

    def get_records(self, ruleset_name: RulesetName) -> list[Record]:
        """Retorna la lista de records de un ruleset."""
        if ruleset_name not in self.rulesets:
            raise ValueError(f"Database: ruleset '{ruleset_name}' no encontrado.")
        return self.rulesets[ruleset_name].records

    def get_top_record(self, ruleset_name: RulesetName) -> Record | None:
        """Retorna el mejor record de un ruleset o None si no hay ninguno."""
        if ruleset_name not in self.rulesets:
            raise ValueError(f"Database: ruleset '{ruleset_name}' no encontrado.")
        return self.rulesets[ruleset_name].top_record

    def reset_records(self, ruleset_name: RulesetName) -> None:
        """Borra todos los records de un ruleset y guarda los cambios."""
        if ruleset_name not in self.rulesets:
            raise ValueError(f"Database: ruleset '{ruleset_name}' no encontrado.")
        self.rulesets[ruleset_name].records.clear()
        self.save()

    def reset_all_records(self) -> None:
        """Borra todos los records de todos los rulesets y guarda los cambios."""
        for ruleset in self.rulesets.values():
            ruleset.records.clear()
        self.save()

    # BUILDERS — JSON -> modelos
    def _build_ruleset(self, name: RulesetName, raw_records: list[RawRecord]) -> RulesetRecords:
        records = [self._dict_to_record(r) for r in raw_records]
        return RulesetRecords(name=name, records=records)

    # SERIALIZACIÓN — modelos -> JSON
    def _record_to_dict(self, record: Record) -> RawRecord:
        return {
            "score":    record.score,
            "lines":    record.lines,
            "level":    record.level,
            "tetrises": record.tetrises,
            "date":     record.date,
        }

    def _dict_to_record(self, raw: RawRecord) -> Record:
        return Record(
            score=raw["score"],
            lines=raw["lines"],
            level=raw["level"],
            tetrises=raw["tetrises"],
            date=raw["date"],
        )

    # HELPERS
    @staticmethod
    def _is_better(new: Record, existing: Record) -> bool:
        """Retorna True si new supera a existing por score DESC, lines como desempate."""
        if new.score != existing.score:
            return new.score > existing.score
        return new.lines > existing.lines