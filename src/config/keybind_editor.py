from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.config.controls_config import ControlsConfig

class KeybindEditor:
    """
    Gestiona la captura y asignación de teclas para ControlsConfig.

    Maneja slots individuales, previene duplicados y conflictos entre acciones
    del mismo contexto. Opera sobre el buffer de ControlsConfig sin guardar
    hasta que se llame a apply().
    """

    def __init__(self, config: "ControlsConfig"):
        self._config    = config
        self._capturing = False
        self._context:  str | None = None
        self._action:   str | None = None
        self._slot:     int | None = None

    # --- ESTADO ---

    @property
    def is_capturing(self) -> bool:
        return self._capturing

    # --- LECTURA ---

    def get_contexts(self) -> list[str]:
        """Devuelve los contextos disponibles (ej: 'play', 'ui')."""
        return self._config.get_contexts()

    def get_actions(self, context: str) -> list[str]:
        """Devuelve las acciones de un contexto."""
        return self._config.get_actions(context)

    def get_keys(self, context: str, action: str) -> set[int]:
        """Devuelve el set de pygame keys asignadas a una acción."""
        return self._config.get(context, action)

    def get_slots(self, context: str, action: str) -> list[int | None]:
        """
        Devuelve lista de tamaño fijo max_keys_for_action.
        Los slots vacíos se rellenan con None.
        """
        keys  = sorted(self._config.get(context, action))
        slots = keys + [None] * (self._config.max_keys_for_action - len(keys))
        return slots[:self._config.max_keys_for_action]

    # --- CAPTURA ---

    def start_capture(self, context: str, action: str, slot: int) -> None:
        """
        Inicia la captura de una tecla para un slot específico.

        Args:
            context: Contexto de la acción (ej: 'play').
            action:  Nombre de la acción (ej: 'move_left').
            slot:    Índice del slot a reasignar (0-based).
        """
        if slot < 0 or slot >= self._config.max_keys_for_action:
            raise ValueError(
                f"KeybindEditor: slot {slot} fuera de rango "
                f"[0-{self._config.max_keys_for_action - 1}]"
            )
        self._context   = context
        self._action    = action
        self._slot      = slot
        self._capturing = True

    def cancel_capture(self) -> None:
        """Cancela la captura sin modificar nada."""
        self._context   = None
        self._action    = None
        self._slot      = None
        self._capturing = False

    def assign(self, key: int) -> None:
        """
        Asigna una tecla al slot en captura.

        Previene duplicados en la misma acción y elimina conflictos
        con otras acciones del mismo contexto.
        """
        if not self._capturing or self._context is None or self._action is None or self._slot is None:
            return

        self._remove_conflicts(key)

        slots = self.get_slots(self._context, self._action)

        # Prevenir duplicado en la misma acción
        if key in slots:
            self.cancel_capture()
            return

        slots[self._slot] = key
        self._config.set(
            {k for k in slots if k is not None},
            self._context, self._action
        )
        self.cancel_capture()

    def clear_slot(self, context: str, action: str, slot: int) -> None:
        """Borra la tecla de un slot específico."""
        if slot < 0 or slot >= self._config.max_keys_for_action:
            raise ValueError(
                f"KeybindEditor: slot {slot} fuera de rango "
                f"[0-{self._config.max_keys_for_action - 1}]"
            )
        slots = self.get_slots(context, action)
        if slots[slot] is None:
            return
        slots[slot] = None
        self._config.set(
            {k for k in slots if k is not None},
            context, action
        )

    # --- CONFIRMACIÓN ---

    def apply(self) -> None:
        """Aplica los cambios del buffer y guarda al JSON."""
        self._config.apply_changes()

    def discard(self) -> None:
        """Descarta todos los cambios pendientes."""
        self._config.discard_changes()

    def has_changes(self) -> bool:
        """True si hay cambios pendientes sin guardar."""
        return self._config.has_changes()

    # --- HELPERS ---

    def _remove_conflicts(self, key: int) -> None:
        """Elimina la tecla de otras acciones del mismo contexto."""
        if self._context is None:
            return
        for action in self._config.get_actions(self._context):
            if action == self._action:
                continue
            keys = self._config.get(self._context, action)
            if key in keys:
                keys.discard(key)
                self._config.set(keys, self._context, action)