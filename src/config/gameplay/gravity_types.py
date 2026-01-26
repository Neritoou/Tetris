from typing import TypedDict

class ExponentialGravityType(TypedDict):
    base_fall_delay: float
    multiplier: float
    min_delay: float

class FixedGravityType(TypedDict):
    fall_delay: float

class ForLevelsGravityType(TypedDict):
    levels: dict[str, float]

class GameplayGravityType(TypedDict):
    exponential: ExponentialGravityType
    fixed: FixedGravityType
    for_levels: ForLevelsGravityType