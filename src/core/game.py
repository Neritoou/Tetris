import pygame
from arcade_machine_sdk import GameBase, GameMeta
from src.resources import ResourceManager
from src.controller import InputManager
from src.audio import AudioManager
from src.states import *
from src.config import *
from src.database import Database
from src.util.paths import get_path

class Game(GameBase):
    def __init__(self, metadata: GameMeta) -> None:
        super().__init__(metadata)
        self.controls_config = ControlsConfig(path = str(get_path("config","controls.json")))
        self.gameplay_config = BaseConfig[GameplayConfigType](path = str(get_path("config","gameplay.json")))
        self.database = Database(get_path("src","database","game_data.json"))
        self.resources = ResourceManager()
        self.audio = AudioManager()
        self.input = InputManager(self.controls_config.data)
        self.state = StateManager(self)


    def start(self, surface: pygame.Surface):
        super().start(surface)
        self.resources.load()
        self.database.load()
        self.state.change(StateID.MENU)
        self.audio.register_sounds(self.resources.get_sounds())

        self.background = self.resources.get_image("Background")

    def handle_events(self, events: list[pygame.event.Event]) -> None:
        self.input.update(events)
        self.state.handle_input(events)

    def update(self, dt: float) -> None:
        self.state.update(dt)

    def render(self) -> None:
        self.state.render(self.surface)