from ..util import OverlayType
from typing import TYPE_CHECKING, Optional
import pygame

if TYPE_CHECKING:
    from game import Game
    from .game_state import GameState



class StateManager:
    """
    Gestiona una pila de estados de juego (stack) con soporte para overlays y estados transitorios.
    """

    def __init__(self,game: "Game"):
        self.stack: list["GameState"] = []
        self.game = game

    @property
    def current(self) -> "GameState":
        """Devuelve el estado superior"""
        if not self.stack:
            # Provisional, se verá después si se maneja de otra forma
            raise ValueError("State Manager: No hay estados en la pila.")
        return self.stack[-1] 
    
    def change(self, state_class: type["GameState"], game: "Game"):
        """
        Reemplaza el estado actual por uno nuevo.

        - Si el nuevo estado NO es un overlay, el estado superior actual es eliminado
        - Si el nuevo estado ES un overlay, se apila sobre el estado actual sin eliminarlo.
        """
        if self.stack and isinstance(self.current, state_class):
            raise ValueError(f"State Manager: El estado {state_class.__name__} ya está activo.")
        
        new_state = state_class(game)
        if new_state.overlay_type == OverlayType.NONE and self.stack:
            self._pop()
        self._push(new_state)

    def _push(self, state: "GameState") -> None:
        """ Agrega un estado al stack y llama a on_enter. """
        self.stack.append(state)
        state.on_enter()

    def _pop(self) -> None:
        """ Elimina el estado superior y llama a on_exit. """
        if self.stack:
            self.current.on_exit()
            self.stack.pop()


    def handle_input(self, events: list[pygame.event.Event]) -> None:
        """Solo el estado superior recibe input"""
        if self.stack:
            self.current.handle_input(events)

    def update(self, dt: float) -> None:
        """
        Actualiza el estado superior no-overlay o el overlay superior.
        Solo el primer estado relevante desde arriba se actualiza.
        """
        if self.stack:
            self.current.update(dt)

    def render(self, surface: pygame.Surface) -> None:
        """
        Renderiza los estados según el overlay del estado superior:
        - Si es FULLSCREEN o NONE, solo renderiza el estado superior.
        - Si permite renderizar fondo, renderiza desde abajo hacia arriba hasta el superior.
        """
        if not self.stack: return
        overlay_type = self.current.overlay_type
        
        # Renderiza el estado actual 
        if overlay_type in (OverlayType.FULLSCREEN, OverlayType.NONE):
            self.current.render(surface)
            return

        # Renderiza los estados por Overlay
        if overlay_type == OverlayType.SEMITRANSPARENT:
            for state in self.stack:
                state.render(surface)
            return

    def clear(self) -> None:
        while self.stack:
            self._pop()

