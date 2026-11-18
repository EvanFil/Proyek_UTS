from abc import ABC, abstractmethod


class Move:
    """Jurus milik Evomon (dibuat di dalam Evomon -> COMPOSITION)."""

    def __init__(self, name, power, element):
        self._name = name
        self._power = power
        self._element = element

    @property
    def name(self):
        return self._name

    @property
    def power(self):
        return self._power

    def __str__(self):
        return f"{self._name} (Power {self._power}, {self._element})"


class EvolveMixin:
    """Kemampuan evolusi, ditempel lewat multiple inheritance."""

    def evolve(self):
        if self.level < 16:
            print(f"{self.name} belum bisa evolusi (butuh Lv 16)")
            return False
        self._attack += 10
        self._max_hp += 20
        self._hp = self._max_hp
        print(f"{self.name} berevolusi! ATK={self._attack}, HP={self._max_hp}")
        return True


class Evomon:
    total_evomon = 0                      # class attribute
    VALID_ELEMENTS = ("Fire", "Water", "Grass")

    def __init__(self, name, element, level, max_hp, attack, move_data):
        if not Evomon.is_valid_element(element):
            raise ValueError(f"Elemen tidak valid: {element}")
        self._name = name
        self._element = element
        self._max_hp = max_hp
        self._hp = max_hp
        self._attack = attack
        self.level = level                # lewat setter
        self._moves = [Move(n, p, element) for (n, p) in move_data]
        Evomon.total_evomon += 1

    @property
    def name(self):
        return self._name

    @property
    def element(self):
        return self._element

    @property
    def hp(self):
        return self._hp

    @property
    def level(self):
        return self._level

    @level.setter
    def level(self, value):
        if not isinstance(value, int) or value < 1 or value > 100:
            raise ValueError("Level harus 1-100")
        self._level = value

    @property
    def is_fainted(self):
        return self._hp == 0

    @staticmethod
    def is_valid_element(e):
        return e in Evomon.VALID_ELEMENTS

    @classmethod
    def starter(cls, name):
        if cls is Evomon:
            raise TypeError("Pakai subclass: FireEvomon/WaterEvomon/GrassEvomon")
        return cls(name, 5, 45, 12, cls.DEFAULT_MOVES)

    def type_multiplier(self, target):
        return 1.0

    def attack_target(self, target, move_index=0):
        move = self._moves[move_index]
        damage = int((move.power + self._attack) * self.type_multiplier(target))
        target.take_damage(damage)
        print(f"{self.name} memakai {move.name} -> {target.name} -{damage} HP (sisa {target.hp})")
        return damage

    def take_damage(self, amount):
        self._hp = max(0, self._hp - amount)

    def __eq__(self, other):
        return (isinstance(other, Evomon) and
                (self._name, self._element, self._level) ==
                (other._name, other._element, other._level))

    def __hash__(self):
        return hash((self._name, self._element, self._level))

    def __str__(self):
        return f"{self._name} [{self._element}] Lv{self._level} HP {self._hp}/{self._max_hp}"


class FireEvomon(Evomon, EvolveMixin):
    DEFAULT_MOVES = [("Flame Burst", 20), ("Tackle", 10)]

    def __init__(self, name, level, max_hp, attack, move_data):
        super().__init__(name, "Fire", level, max_hp, attack, move_data)

    def type_multiplier(self, target):
        if target.element == "Grass":
            return 1.5
        if target.element == "Water":
            return 0.5
        return 1.0


class WaterEvomon(Evomon, EvolveMixin):
    DEFAULT_MOVES = [("Aqua Jet", 20), ("Tackle", 10)]

    def __init__(self, name, level, max_hp, attack, move_data):
        super().__init__(name, "Water", level, max_hp, attack, move_data)

    def type_multiplier(self, target):
        if target.element == "Fire":
            return 1.5
        if target.element == "Grass":
            return 0.5
        return 1.0


class GrassEvomon(Evomon, EvolveMixin):
    DEFAULT_MOVES = [("Leaf Storm", 20), ("Tackle", 10)]

    def __init__(self, name, level, max_hp, attack, move_data):
        super().__init__(name, "Grass", level, max_hp, attack, move_data)

    def type_multiplier(self, target):
        if target.element == "Water":
            return 1.5
        if target.element == "Fire":
            return 0.5
        return 1.0


class BattleSide(ABC):
    """Pihak yang bertarung (Trainer atau Evomon liar)."""

    def __init__(self, name):
        self._name = name

    @property
    def name(self):
        return self._name

    @abstractmethod
    def first_alive(self):
        pass


class Trainer(BattleSide):
    MAX_TEAM = 5

    def __init__(self, name, coins):
        super().__init__(name)
        self.coins = coins                # lewat setter
        self._team = []

    @property
    def coins(self):
        return self._coins

    @coins.setter
    def coins(self, value):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Coins tidak boleh negatif")
        self._coins = value

    def add_evomon(self, e):              # AGGREGATION
        if len(self._team) >= Trainer.MAX_TEAM:
            raise ValueError("Tim penuh")
        self._team.append(e)

    def first_alive(self):
        for e in self._team:
            if not e.is_fainted:
                return e
        return None

    def __str__(self):
        return f"Trainer {self._name} ({len(self._team)} Evomon, {self._coins} coins)"


class WildEncounter(BattleSide):
    def __init__(self, evomon):           # AGGREGATION: evomon dibuat di luar
        super().__init__("Evomon Liar")
        self._evomon = evomon

    def first_alive(self):
        if not self._evomon.is_fainted:
            return self._evomon
        return None


class Battle:
    def __init__(self, side_a, side_b):   # ASSOCIATION
        self._side_a = side_a
        self._side_b = side_b

    def run(self):
        turn = 1
        while self._side_a.first_alive() is not None and self._side_b.first_alive() is not None:
            print(f"--- Turn {turn} ---")
            a = self._side_a.first_alive()
            b = self._side_b.first_alive()
            a.attack_target(b, 0)
            if not b.is_fainted:
                b.attack_target(a, 0)
            turn += 1
        winner = self._side_a if self._side_a.first_alive() is not None else self._side_b
        print(f"Pemenang: {winner.name}")
        return winner


if __name__ == "__main__":
    ash = Trainer("Ash", 100)
    gary = Trainer("Gary", 100)
    flamy = FireEvomon.starter("Flamy")
    leafy = GrassEvomon.starter("Leafy")
    aquaro = WaterEvomon.starter("Aquaro")
    ash.add_evomon(flamy)
    ash.add_evomon(leafy)
    gary.add_evomon(aquaro)

    print(ash)
    print(gary)
    print(flamy)
    print(f"Total Evomon: {Evomon.total_evomon}")

    # percobaan nilai tidak valid (validasi setter)
    try:
        flamy.level = 150
    except ValueError as err:
        print(f"Error: {err}")
    try:
        ash.coins = -50
    except ValueError as err:
        print(f"Error: {err}")

    # perbandingan dua object dengan ==
    clone = FireEvomon.starter("Flamy")
    print(f"flamy == clone  : {flamy == clone}")
    print(f"flamy == aquaro : {flamy == aquaro}")
    print("MRO: [" + ", ".join(c.__name__ for c in FireEvomon.__mro__) + "]")

    # skenario: Trainer vs Trainer
    Battle(ash, gary).run()
    print(flamy)
    flamy.evolve()
    del ash                                # AGGREGATION: Evomon tetap ada
    print(f"Setelah Ash dihapus: {leafy}")

    # skenario: Trainer vs Evomon liar (polymorphism)
    brock = Trainer("Brock", 50)
    brock.add_evomon(GrassEvomon.starter("Bushy"))
    wild = WildEncounter(WaterEvomon.starter("Wildy"))
    print("=== Battle melawan Evomon liar ===")
    Battle(brock, wild).run()
