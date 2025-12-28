import pygame
from arcade_machine_sdk import GameBase, GameMeta
from ..resources import ResourceManager
from ..controller import InputManager
from ..states import StateManager, PlayState

class Game(GameBase):
    def __init__(self, metadata: GameMeta) -> None:
        super().__init__(metadata)
        self.resource_manager: ResourceManager = ResourceManager()
        self.input: InputManager = InputManager("config/controls.json")
        self.state: StateManager = StateManager(self)
 


    def start(self, surface: pygame.Surface):
        super().start(surface)
        # Cargar Recursos 
        self.resource_manager.load_resources()
        # Estado inicial       
        self.state.change(PlayState)

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        self.input.update(events)
        self.state.handle_input(events)

    def update(self, dt: float) -> None:
        self.state.update(dt)

    def render(self) -> None:
        self.surface.fill((0, 0, 0))
        self.state.render(self.surface)