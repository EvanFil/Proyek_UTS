

class EvomonError(Exception): #Base
    """Base exception: semua kesalahan khusus aplikasi Evomon."""


#  Data tidak valid 
class ValidationError(EvomonError):
    """Data yang dimasukkan tidak valid."""


class InvalidLevelError(ValidationError):
    """Level di luar 1-100 atau bukan integer."""

    def __init__(self, value, min_level=1, max_level=100):
        self.value = value
        self.min_level = min_level
        self.max_level = max_level
        super().__init__(
            f"Level harus bilangan bulat {min_level}-{max_level}, diberikan: {value!r}"
        )


class InvalidCoinsError(ValidationError):
    """Coins negatif atau bukan integer."""

    def __init__(self, value):
        self.value = value
        super().__init__(
            f"Coins harus bilangan bulat >= 0 (tidak boleh negatif), diberikan: {value!r}"
        )


class InvalidElementError(ValidationError):
    """Elemen bukan Fire, Water, atau Grass."""

    def __init__(self, element, valid_elements=("Fire", "Water", "Grass")):
        self.element = element
        self.valid_elements = valid_elements
        super().__init__(
            f"Elemen '{element}' tidak valid. Pilihan elemen sah: {', '.join(valid_elements)}"
        )


# Aturan permainan dilanggar 
class RuleViolationError(EvomonError):
    """Aturan permainan dilanggar."""


class TeamFullError(RuleViolationError):
    """Tim Trainer sudah penuh."""

    def __init__(self, trainer_name, max_team):
        self.trainer_name = trainer_name
        self.max_team = max_team
        super().__init__(
            f"Tim Trainer {trainer_name} sudah penuh (maksimal {max_team} Evomon)"
        )


class FaintedEvomonError(RuleViolationError):
    """Evomon yang pingsan tidak boleh menyerang atau diserang."""

    def __init__(self, evomon_name, role="menyerang"):
        self.evomon_name = evomon_name
        self.role = role
        super().__init__(
            f"{evomon_name} sudah pingsan (HP 0) dan tidak bisa {role}"
        )


class EvolutionNotAllowedError(RuleViolationError):
    """Syarat evolusi belum terpenuhi."""

    def __init__(self, evomon_name, current_level, required_level=16):
        self.evomon_name = evomon_name
        self.current_level = current_level
        self.required_level = required_level
        self.missing_levels = required_level - current_level
        super().__init__(
            f"{evomon_name} (Lv{current_level}) belum bisa evolusi "
            f"(butuh Lv{required_level}, kurang {self.missing_levels} level)"
        )


class MoveNotFoundError(RuleViolationError):
    """Indeks jurus tidak tersedia pada Evomon."""

    def __init__(self, evomon_name, move_index, total_moves):
        self.evomon_name = evomon_name
        self.move_index = move_index
        self.total_moves = total_moves
        super().__init__(
            f"{evomon_name} tidak memiliki jurus pada indeks ke-{move_index} "
            f"(tersedia {total_moves} jurus)"
        )