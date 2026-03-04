from typing import TYPE_CHECKING
import pygame

if TYPE_CHECKING:
    from src.config import GameplayConfigType


class Score:
    """
    Calcula y almacena el puntaje del jugador basándose en la configuración
    del gameplay.
    """
    def __init__(self, gameplay_config: "GameplayConfigType"):
        self.config = gameplay_config
        self.current_score: int  = 0
        self.aux_score: int  = 0
        self.combo_count: int  = 0
        self.back_to_back_active: bool = False
        self.level: int  = self.config["general"]["starting_level"]
        self.lines_cleared_total: int = 0
        self.tetrises: int = 0


        self.soft_drop: int = 0
        self.prev_soft_drop: int = 0

        self.hard_drop: int = 0
        self.prev_hard_drop: int = 0

        self.debug_lines_cleared = 0  # (!) QUITAR
        self.debug_move_type = ""     # (!) QUITAR

    def update(self, lines_cleared: int, move_type: str) -> None:
        self.prev_soft_drop = self.soft_drop
        self.prev_hard_drop = self.hard_drop
        self.aux_score = 0


        self.debug_move_type = move_type          # (!) QUITAR
        self.debug_lines_cleared = lines_cleared  # (!) QUITAR

        if self.soft_drop > 0: self.apply_soft_drop(self.soft_drop)
        if self.hard_drop > 0: self.apply_hard_drop(self.hard_drop)
        self.hard_drop = 0
        self.soft_drop = 0

        if lines_cleared:
            self.lines_cleared_total += lines_cleared
            if lines_cleared == 4: self.tetrises += 1
            self.apply_lines_cleared(lines_cleared, move_type)
            self.apply_back_to_back(lines_cleared, move_type)
            self.apply_combo()
            self.level_up()
        else:
            self.combo_count = 0
            self.back_to_back_active = False  # se resetea si no se eliminaron líneas

        self.current_score += self.aux_score

    def apply_combo(self) -> None:
        """Suma puntos por combo. El primer clear no da bonus."""
        if self.combo_count > 0:  # el primer clear (combo_count == 0) no otorga bonus
            self.aux_score += self.config["score"]["combo_bonus"] * self.combo_count * self.level
        self.combo_count += 1  # se incrementa después del cálculo

    def apply_back_to_back(self, lines_cleared, move_type: str) -> None:
        """Multiplica los puntos base si se encadenan jugadas difíciles."""
        is_difficult = (lines_cleared == 4) or (move_type in ("t_spin", "mini_t_spin"))

        if is_difficult and self.back_to_back_active:
            self.aux_score = int(self.aux_score * self.config["score"]["back_to_back_multiplier"])

        # Activa el flag si fue difícil, lo resetea si fue clear normal
        self.back_to_back_active = is_difficult

    def apply_soft_drop(self, lines_dropped: int) -> None:
        """Suma puntos por soft drop."""
        self.aux_score += self.config["score"]["soft_drop"] * lines_dropped

    def apply_hard_drop(self, lines_dropped: int) -> None:
        """Suma puntos por hard drop."""
        self.aux_score += self.config["score"]["hard_drop"] * lines_dropped

    def apply_lines_cleared(self, lines_cleared: int, move_type: str) -> None:
        """Despacha al método correspondiente según el tipo de jugada."""
        if move_type == "t_spin":
            self._apply_t_spin(lines_cleared)
        elif move_type == "mini_t_spin":
            self._apply_mini_t_spin(lines_cleared)
        else:
            self._apply_normal(lines_cleared)

    def _apply_normal(self, lines_cleared: int) -> None:
        """Suma puntos por líneas normales (single, double, triple, tetris)."""
        key = str(lines_cleared)
        if key in self.config["score"]["normal"]:
            self.aux_score += self.config["score"]["normal"][key] * self.level

    def _apply_t_spin(self, lines_cleared: int) -> None:
        """Suma puntos por T-spin."""
        key = str(lines_cleared)
        if key in self.config["score"]["t_spin"]:
            self.aux_score += self.config["score"]["t_spin"][key] * self.level

    def _apply_mini_t_spin(self, lines_cleared: int) -> None:
        """Suma puntos por Mini T-spin."""
        key = str(lines_cleared)
        if key in self.config["score"]["mini_t_spin"]:
            self.aux_score += self.config["score"]["mini_t_spin"][key] * self.level

    def get_score(self) -> int:
        """Devuelve el puntaje actual."""
        return self.current_score

    def level_up(self) -> None:
        """Actualiza el nivel según las líneas eliminadas."""
        self.level = self.lines_cleared_total // self.config["general"]["lines_per_level"] + 1

    def debug_draw(self, surface: pygame.Surface, font: pygame.font.Font,
                   fall: tuple[float, float], lock: tuple[float, float],
                   pos_x: int = 10, pos_y: int = 10, line_height: int = 25) -> None:
        debug_texts = [
            "ACTUAL SCORE:",
            f"Current Score: {self.current_score}",
            f"Aux Score: {self.aux_score}",
            f"Combo Count: {self.combo_count}",
            f"Back-to-Back: {self.back_to_back_active}",
            f"Level: {self.level}",
            f"Lines Cleared Total: {self.lines_cleared_total}",
            f"Fall Delay: {fall[0]:.3f}",
            f"Fall Timer: {fall[1]:.3f}",
            f"Lock Delay: {lock[0]:.3f}",
            f"Lock Timer: {lock[1]:.3f}",
            "", "", "CHANGES:",
            f"Previous Soft Drop: {self.prev_soft_drop} x{self.config['score']['soft_drop']} ({self.prev_soft_drop * self.config['score']['soft_drop']})",
            f"Previous Hard Drop: {self.prev_hard_drop} x{self.config['score']['hard_drop']} ({self.prev_hard_drop * self.config['score']['hard_drop']})",
            f"Previous Lines Cleared: {self.debug_lines_cleared}",
            f"Previous Move Type: {self.debug_move_type}",
        ]

        for i, text in enumerate(debug_texts):
            rendered = font.render(text, True, (255, 255, 255))
            surface.blit(rendered, (pos_x, pos_y + i * line_height))