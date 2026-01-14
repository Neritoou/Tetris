from typing import Dict, Type, TYPE_CHECKING

if TYPE_CHECKING:
    from ...config.gameplay import GameplayRulesetType, GameplayConfigType
    from .gravity_strategy import GravityStrategy
    from .lock_strategy import LockStrategy

from .gravity_strategy import (
    ExponentialGravity,
    FixedGravity,
    ForLevelsGravity
)
from .lock_strategy import (
    AutoLock,
    FixedLock,
    ResettableLock,
    CollisionDelayLock
)

# Ruleset keys
GRAVITY_KEY = "gravity_type"
LOCK_KEY = "lock_type"

GRAVITY_CONFIG_KEY = "gravity_types"
LOCK_CONFIG_KEY = "lock_types"

# Strategy maps
GRAVITY_MAP: "Dict[str, Type[GravityStrategy]]" = {
    "exponential": ExponentialGravity,
    "fixed": FixedGravity,
    "for_levels": ForLevelsGravity,
}

LOCK_MAP: "Dict[str, Type[LockStrategy]]" = {
    "auto": AutoLock,
    "fixed": FixedLock,
    "resettable": ResettableLock,
    "collision_delay": CollisionDelayLock,
}

# Factory API
def create_gravity(ruleset: "GameplayRulesetType", config: "GameplayConfigType"):
    _validate_gravity(ruleset, config)

    g_type = ruleset[GRAVITY_KEY]
    gravity_cfg = config[GRAVITY_CONFIG_KEY][g_type]
    gravity_class = GRAVITY_MAP[g_type]         

    return gravity_class(g_type, gravity_cfg)  

def create_lock(ruleset: "GameplayRulesetType", config: "GameplayConfigType"):
    _validate_lock(ruleset, config)

    l_type = ruleset[LOCK_KEY]
    lock_cfg = config[LOCK_CONFIG_KEY][l_type]
    lock_class = LOCK_MAP[l_type]

    return lock_class(l_type,lock_cfg)

# --- HELPERS ----
def _validate_gravity(ruleset: "GameplayRulesetType", config: "GameplayConfigType") -> None:
    if GRAVITY_KEY not in ruleset:
        raise ValueError(f"Rules Factory: Ruleset inválido, falta '{GRAVITY_KEY}'")

    g_type = ruleset[GRAVITY_KEY]

    if g_type not in GRAVITY_MAP:
        raise ValueError(f"Rules Factory: Gravity '{g_type}' no está registrada en GRAVITY_MAP")

    if g_type not in config[GRAVITY_CONFIG_KEY]:
        raise ValueError(f"Rules Factory: Gravity '{g_type}' no existe en config[{GRAVITY_CONFIG_KEY}]")


def _validate_lock(ruleset: "GameplayRulesetType", config: "GameplayConfigType") -> None:
    if LOCK_KEY not in ruleset:
        raise ValueError(f"Rules Factory: Ruleset inválido, falta '{LOCK_KEY}'")

    l_type = ruleset[LOCK_KEY]

    if l_type not in LOCK_MAP:
        raise ValueError(f"Rules Factory: Lock '{l_type}' no está registrado en LOCK_MAP")

    if l_type not in config[LOCK_CONFIG_KEY]:
        raise ValueError(f"Rules Factory: Lock '{l_type}' no existe en config[{LOCK_CONFIG_KEY}]")
