from typing import TypedDict

class AutoLockType(TypedDict):
    lock_delay: float

class FixedLockType(TypedDict):
    lock_delay: float

class ResettableLockType(TypedDict):
    lock_delay: float
    max_moves: int

class CollisionDelayLockType(TypedDict):
    lock_delay: float

class GameplayLockType(TypedDict):
    auto: AutoLockType
    fixed: FixedLockType
    resettable: ResettableLockType
    colission_delay: CollisionDelayLockType