from typing import Optional, Dict, Any

# (!) NO ES FUNCIONAL AÚN
class Score:
    """
    Calcula y almacena el puntaje del jugador basándose en la configuración
    del gameplay.
    """
    def __init__(self, gameplay_config: Dict[Any, Any]):
        """
        :param gameplay_config: instancia de GameplayConfig (BaseConfig)
        """
        self.config = gameplay_config
        self.current_score = 0
        self.combo_count = 0
        self.back_to_back_active = False
        self.level = self.config["general"]["starting_level"]
        self.lines_cleared_total = 0

    def update(self, lines_cleared: int, t_spin: bool, t_mini_spin: bool):
        pass
            
    def add_soft_drop(self, lines_dropped: int = 1):
        """Suma puntos por soft drop"""
        self.current_score += self.config["score"]["soft_drop"] * lines_dropped

    def add_hard_drop(self, lines_dropped: int):
        """Suma puntos por hard drop"""
        self.current_score += self.config["score"]["hard_drop"] * lines_dropped

    def add_combo_bonus(self):
        """Suma puntos por combo"""
        if self.combo_count > 1:
            self.current_score += self.combo_count * self.config["score"]["combo_bonus"]

    def add_back_to_back(self):
        """Suma puntos por back-to-back"""
        if self.back_to_back_active:
            self.current_score += self.config["score"]["back_to_back_multiplier"]

    def add_lines_cleared(self, lines_cleared: int, line_type: str):
        """Suma puntos por las líneas eliminadas (single, double, triple, tetris, etc.)"""
        if line_type in self.config["lines_cleared"]:
            line_score = self.config["lines_cleared"][line_type] * lines_cleared
            self.current_score += line_score
            self.lines_cleared_total += lines_cleared

    def add_t_spin(self, spin_type: str, lines_cleared: int = 1):
        """Suma puntos por T-Spins (normal, single, double, triple)"""
        if spin_type in self.config["t_spin"]:
            spin_score = self.config["t_spin"][spin_type] * lines_cleared
            self.current_score += spin_score

    def add_mini_t_spin(self, spin_type: str, lines_cleared: int = 1):
        """Suma puntos por Mini T-Spins"""
        if spin_type in self.config["mini_t_spin"]:
            mini_spin_score = self.config["mini_t_spin"][spin_type] * lines_cleared
            self.current_score += mini_spin_score

    def add_back_to_back_t_spin(self, spin_type: str):
        """Suma puntos por back-to-back T-Spins"""
        if spin_type in self.config["back_to_back"]:
            self.current_score += self.config["back_to_back"][spin_type]

    def reset_combo(self):
        """Resetea el combo si no hubo línea clara"""
        self.combo_count = 0

    def get_score(self) -> int:
        """Devuelve el puntaje actual"""
        return self.current_score

    def level_up(self):
        self.level = self.lines_cleared_total // self.config["general"]["lines_per_level"] + 1