from .game_state import GameState
from ..util import OverlayType
import pygame

class StateManager:
    """
    Gestiona una pila de estados de juego (stack) con soporte para overlays y estados transitorios.
    """

    def __init__(self):
        self.stack: list[GameState] = []

    @property
    def current(self) -> GameState:
        """Devuelve el estado superior"""
        return self.stack[-1] 
    
    def push(self, state: GameState) -> None:
        """
        Agrega un estado al stack y llama a on_enter.
        Si el estado es un overlay, no elimina el estado anterior.
        """
        if state.overlay_type == OverlayType.NONE and self.stack:
            self.current.on_exit()
        self.stack.append(state)
        state.on_enter()

    def pop(self) -> None:
        """
        Elimina el estado superior y llama a on_exit.
        Si el estado superior es un overlay, solo se elimina el overlay y se mantiene el estado anterior.
        """
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
            self.pop()

