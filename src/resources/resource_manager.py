import pygame
import numpy as np
from typing import Dict, Tuple, TypeVar, TYPE_CHECKING
from .spritesheet import SpriteSheet
from .piece_library import PieceLibrary
from ..constants import PIECE_DEFINITIONS, BLOCK_W, BLOCK_H, BLOCK_PW, BLOCK_PH

if TYPE_CHECKING:
    from .piece_library import PieceData, PieceSurfaces

T = TypeVar("T")
K = TypeVar("K")

class ResourceManager:
    """Gestor de recursos del juego: imágenes, sonidos, fuentes, spritesheets y piezas."""


    def __init__(self):
        """Inicializa los contenedores de recursos vacíos."""
        self.images: Dict[str, pygame.Surface] = {}
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.fonts: Dict[Tuple[str,int], pygame.font.Font] = {}
        self.spritesheets: Dict[str, SpriteSheet] = {}
        self.piece_library: PieceLibrary = PieceLibrary()
    # (?) MEJORAR ESTO



    # --- LOADERS ---
    def load_image(self, key: str, path: str) -> None:
        """Carga y almacena una imagen desde disco."""
        self._assert_not_loaded(self.images,key,"Image")
        img = pygame.image.load(path)
        self.images[key] = img.convert_alpha() if img.get_alpha() else img.convert()

    def load_sound(self, key: str, path: str) -> None:
        """Carga y almacena un sonido."""
        self._assert_not_loaded(self.sounds,key,"Sound")
        self.sounds[key] = pygame.mixer.Sound(path)

    def load_font(self, key: str, path: str, size: int) -> None:
        """Carga y almacena una fuente."""
        self._assert_not_loaded(self.fonts, (key,size), "Font")
        self.fonts[(key,size)] = pygame.font.Font(path, size)

    def load_spritesheet(self, key: str, path: str, frame_size: Tuple[int,int], padding: Tuple[int,int] = (0,0)) -> None:
        """Carga un spritesheet desde disco."""
        self._assert_not_loaded(self.spritesheets,key,"SpriteSheet")
        image = pygame.image.load(path).convert_alpha()
        self.spritesheets[key] = SpriteSheet(image,frame_size,padding)

    def load_piece(self, key: str, base_matrix: np.ndarray, blocks: "PieceSurfaces") -> None:
        """Registra una pieza en la biblioteca interna."""
        self.piece_library.register_piece(key, base_matrix,blocks)



    # --- GETTERS ---
    def get_image(self, key: str) -> pygame.Surface:
        """Obtiene una imagen cargada."""
        return self._get_resource(self.images, key, "Image")

    def get_sound(self, key: str) -> pygame.mixer.Sound:
        """Obtiene un sonido cargado."""
        return self._get_resource(self.sounds, key, "Sound")

    def get_font(self, key: str, size: int) -> pygame.font.Font:
        return self._get_resource(self.fonts, (key, size), "Font")
    
    def get_spritesheet(self, key: str) -> SpriteSheet:
        """Obtiene un spritesheet cargado."""
        return self._get_resource(self.spritesheets, key, "SpriteSheet")
    
    def get_piece(self, key: str) -> "PieceData":
        """Obtiene una pieza registrada en la biblioteca."""
        return self.piece_library.get_piece(key)
    # (?) MEJORAR ESTO



    # --- CARGA GLOBAL DE RECURSOS ---
    def load_resources(self):
        """Carga todos los recursos y piezas del juego."""
        self.__load_spritesheets()
        self.__load_images()
        self.__load_fonts()
        self.__load_sounds()
        self.__load_pieces()

    # --- MÉTODOS PRIVADOS DE CARGA ---
    def __load_images(self) -> None:
        # BOARD BASE
        self.load_image("Board","assets/images/grid.png")

    def __load_fonts(self) -> None:
        pass

    def __load_sounds(self) -> None:
        pass

    def __load_spritesheets(self) -> None:
        # BLOQUES PARA LAS PIEZAS
        self.load_spritesheet("BlocksType", "assets/spritesheets/tetromino.png", (BLOCK_W,BLOCK_H), (BLOCK_PW,BLOCK_PH))
    
    def __load_pieces(self) -> None:
        """Registra las piezas del Tetris usando la constante PIECE_DEFINITIONS."""
        sheet = self.get_spritesheet("BlocksType") 

        # Se itera en la Constante para obtener los datos de la Pieza
        for name, info in PIECE_DEFINITIONS.items():
            col = info["spritesheet_col"] 
            base_matrix = info["matrix"]

            # Se obtiene directamente las Surfaces de los Bloques para la Pieza
            frames = sheet.get_frames_at_col(col) 
            # Se asignan a su respectivo diccionario
            blocks: PieceSurfaces = {
                "normal": frames[0],
                "placed": frames[1],
                "ghost": frames[2]
            }
            self.load_piece(name, base_matrix, blocks)



    # --- HELPERS ---
    def _assert_not_loaded(self, container: Dict[K, T], key: K, resource_type: str) -> None:
        """Verifica que un recurso no esté previamente cargado."""
        if key in container:
            raise ValueError(f"ResourceManager: {resource_type} '{key}' ya está cargado")


    def _get_resource(self, container: Dict[K, T], key: K, resource_type: str) -> T:
        """Obtiene un recurso de un diccionario, lanzando KeyError si no existe."""
        if key not in container:
            raise KeyError(f"Resource Manager: {resource_type} '{key}' no está cargado")
        return container[key]