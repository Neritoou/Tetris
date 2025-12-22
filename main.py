from game import Game
from arcade_machine_sdk import GameMeta
import pygame

if not pygame.get_init():
    pygame.init()

metadata = (GameMeta()
            .with_title("Tetris")
            .with_description("Juego de prueba")
            .with_release_date("16/12/2025")
            .with_group_number(1)
            .add_tag("Plataforma")
            .add_author("Agostinho Dos Santos")
            .add_author("Odett Sayegh"))

game = Game(metadata)

if __name__ == "__main__":
    game.run_independently()