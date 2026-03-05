from typing import TypedDict
from src.config.gameplay.gravity_types import GameplayGravityType
from src.config.gameplay.lock_types import GameplayLockType

class GameplayGeneralType(TypedDict):
    starting_level: int
    lines_per_level: int
    bag_size: int
    preview_count: int

class GameplayRulesetType(TypedDict):
    display_name: str
    description: str
    gravity_type: str
    lock_type:    str
    hold:         bool
    wall_kicks:   bool

class GameplayScoreType(TypedDict):
    soft_drop: int
    hard_drop: int
    combo_bonus: int
    back_to_back_multiplier: float
    normal: dict[str, int]
    t_spin: dict[str, int]
    mini_t_spin: dict[str, int]

class GameplayConfigType(TypedDict):
    general: GameplayGeneralType
    rulesets: dict[str, GameplayRulesetType]  # Porque puede haber múltiples reglas
    score: GameplayScoreType
    gravity_types: GameplayGravityType
    lock_types: GameplayLockType