from typing import Dict, Any
import pygame

# (!) NO ES FUNCIONAL AÚN
class Score:
    """
    Calcula y almacena el puntaje del jugador basándose en la configuración
    del gameplay.
    """
    def __init__(self, gameplay_config: Dict[Any, Any]):
        """
        :param gameplay_config: Data de GameplayConfig 
        """
        self.config = gameplay_config
        self.current_score = 0
        self.aux_score = 0
        self.combo_count = 0
        self.back_to_back_active = False
        self.level = self.config["general"]["starting_level"]
        self.lines_cleared_total = 0

        self.debug_soft_drop = 0 # (!) QUITAR
        self.debug_hard_drop = 0 # (!) QUITAR
        self.debug_lines_cleared = 0 # (!) QUITAR
        self.debug_type_moviment = "" # (!) QUITAR

    def update(self, lines_cleared: int, type: str, soft_drop: int, hard_drop: int):
        """
        Actualiza el puntaje del jugador según:
        - lines_cleared: número de líneas eliminadas
        - type: tipo de jugada ("normal", "t_spin", "t_mini_spin")
        - soft_drop: filas descendidas con soft drop
        - hard_drop: filas descendidas con hard drop
        """
        self.aux_score = 0 # Resetear el puntaje temporal
        self.debug_hard_drop = 0 # (!) QUITAR
        self.debug_soft_drop = 0 # (!) QUITAR
        self.debug_type_moviment = type # (!) QUITAR
        self.debug_lines_cleared = lines_cleared  # (!) QUITAR
        if soft_drop > 0: self.apply_soft_drop(soft_drop)
        if hard_drop > 0: self.apply_hard_drop(hard_drop)

        if lines_cleared:
   
            self.lines_cleared_total += lines_cleared
            self.apply_lines_cleared(lines_cleared, type)

            self.apply_back_to_back()
            self.apply_combo()
            self.level_up()
        else:
            self.combo_count  = 0 # Resetear combo si no se eliminaron líneas
           
        self.current_score += self.aux_score

    def apply_combo(self) -> None:
        """Suma puntos por combo"""
        self.aux_score += (self.combo_count + self.config["score"]["combo_bonus"]) * self.level
        self.combo_count += 1

    def apply_back_to_back(self):
        """Suma puntos por back-to-back"""
        if self.back_to_back_active:
            self.aux_score *= self.config["score"]["back_to_back_multiplier"]
        return self.aux_score
    
    def apply_soft_drop(self, lines_dropped: int = 1):
        """Suma puntos por soft drop"""
        self.aux_score += self.config["score"]["soft_drop"] * lines_dropped
        self.debug_soft_drop =  self.config["score"]["soft_drop"] * lines_dropped # (!) QUITAR

    def apply_hard_drop(self, lines_dropped: int):
        """Suma puntos por hard drop"""
        self.aux_score += self.config["score"]["hard_drop"] * lines_dropped
        self.debug_hard_drop = self.config["score"]["hard_drop"] * lines_dropped # (!) QUITAR

    def apply_lines_cleared(self, lines_cleared: int, type: str):
        """
        Aplica los puntos según el tipo de jugada (normal, t_spin, mini_t_spin)
        """
        # Diccionario de funciones para cada tipo de jugada
        type_functions = {
            "normal": self.apply_normal,
            "t_spin": self.apply_t_spin,
            "t_mini_spin": self.apply_mini_t_spin
        }

        # Llamada a la función correspondiente según el tipo
        if type in type_functions:
            type_functions[type](lines_cleared)

    def apply_normal(self, lines_cleared: int):
        """Suma puntos por las líneas eliminadas (single, double, triple, tetris, etc.)"""
        line_score = self.config["normal"][str(lines_cleared)] * lines_cleared * self.level
        self.aux_score += line_score

    def apply_t_spin(self, lines_cleared: int):
        """Suma puntos por T-Spins (normal, single, double, triple)"""
        spin_score = self.config["t_spin"][str(lines_cleared)] * lines_cleared * self.level
        self.aux_score += spin_score

    def apply_mini_t_spin(self, lines_cleared: int):
        """Suma puntos por Mini T-Spins"""
        mini_spin_score = self.config["mini_t_spin"][str(lines_cleared)] * lines_cleared * self.level
        self.aux_score += mini_spin_score

    def get_score(self) -> int:
        """Devuelve el puntaje actual"""
        return self.current_score

    def level_up(self):
        """Actualiza el nivel según las líneas eliminadas"""
        self.level = self.lines_cleared_total // self.config["general"]["lines_per_level"] + 1


    def debug_draw(self, surface: pygame.Surface, font: pygame.font.Font, pos_x: int = 10, pos_y: int = 10, line_height: int = 25) -> None:
        """
        Dibuja en la pantalla los valores internos del Score para debug.

        Args:
            surface: Surface de pygame donde dibujar.
            font: Fuente de pygame para renderizar texto.
            pos_x, pos_y: Coordenadas iniciales donde empezar a dibujar.
            line_height: Altura entre líneas de texto.
        """
        debug_texts = [
            f"ACTUAL SCORE:",
            f"Current Score: {self.current_score}",
            f"Aux Score: {self.aux_score}",
            f"Combo Count: {self.combo_count}",
            f"Back-to-Back: {self.back_to_back_active}",
            f"Level: {self.level}",
            f"Lines Cleared Total: {self.lines_cleared_total}",
            f"", f"", f"CHANGES:",
            f"Previous Soft Drop: {self.debug_soft_drop}",
            f"Previous Hard Drop: {self.debug_hard_drop}",
            f"Previous Lines Cleared: {self.debug_lines_cleared}",
            f"Previous Type Moviment {self.debug_type_moviment}"
        ]

        for i, text in enumerate(debug_texts):
            rendered = font.render(text, True, (255, 255, 255))
            surface.blit(rendered, (pos_x, pos_y + i * line_height))