import pygame

class SpriteSheet:
    def __init__(self, image: pygame.Surface, frame_size: tuple[int,int], padding: tuple[int,int] = (0,0)) -> None:
        self._image: pygame.Surface = image
        self._w: int = image.get_width()
        self._h: int = image.get_height()
        self._padding_w = padding[0]
        self._padding_h = padding[1]

        self._assert_valid_width(frame_size[0])
        self._assert_valid_height(frame_size[1])

        self._fw: int = frame_size[0]
        self._fh: int = frame_size[1]

        self._cols: int = self._w // self._fw
        self._rows: int = self._h // self._fh
    
    def get_frame_at(self, row: int, col: int) -> pygame.Surface:
        self._assert_valid_row(row)
        self._assert_valid_col(col)

        x = col * (self._fw + 2 * self._padding_w) + self._padding_w
        y = row * (self._fh + 2 * self._padding_h) + self._padding_h

        return self._image.subsurface((x, y, self._fw, self._fh))

    def get_frames_at_row(self, row: int) -> list[pygame.Surface]:
        self._assert_valid_row(row)
        frames = []
        for col in range(self._cols):
            x = col * (self._fw + 2 * self._padding_w) + self._padding_w
            y = row * (self._fh + 2 * self._padding_h) + self._padding_h
            frames.append(self._image.subsurface((x, y, self._fw, self._fh)))
        return frames


    def get_frames_at_col(self, col: int) -> list[pygame.Surface]:
        self._assert_valid_col(col)
        frames = []
        for row in range(self._rows):
            x = col * (self._fw + 2 * self._padding_w) + self._padding_w
            y = row * (self._fh + 2 * self._padding_h) + self._padding_h
            frames.append(self._image.subsurface((x, y, self._fw, self._fh)))
        return frames


    def _assert_valid_row(self, row: int) -> None:
        if row < 0 or row >= self._rows:
            raise IndexError(f"Fila {row} fuera del rango [0-{self._rows - 1}]")

    def _assert_valid_col(self, col: int) -> None:
        if col < 0 or col >= self._cols:
            raise IndexError(f"Columna {col} fuera del rango [0-{self._cols - 1}]")
        
    def _assert_valid_height(self, frame_height: int) -> None:
        if self._h % (frame_height + 2*self._padding_h) != 0:
            raise ValueError(f"Spritesheet inválido: alto {self._h} no es múltiplo de {frame_height}")

    def _assert_valid_width(self, frame_width: int) -> None:
        if self._w % (frame_width + 2*self._padding_w) != 0:
            raise ValueError(f"Spritesheet inválido: ancho {self._w} no es múltiplo de {frame_width}")

    @property
    def rows(self):
        return self._rows
    
    @property
    def cols(self):
        return self._cols
    
    @property
    def width(self):
        return self._w
    
    @property 
    def height(self):
        return self._h
    
    @property
    def frame_width(self):
        return self._fw
    
    @property
    def frame_height(self):
        return self._fh