from abc import ABC, abstractmethod                                 # ambil alat untuk membuat 'kerangka' (abstract)


class Move:                                                         # CETAKAN JURUS
    """Jurus milik Evomon (dibuat di dalam Evomon -> COMPOSITION)."""  # catatan: jurus lahir di dalam monster (composition)

    def __init__(self, name, power, element):                       # proses LAHIR jurus: butuh nama, kekuatan, elemen
        self._name = name                                           # catat nama di kartu jurus
        self._power = power                                         # catat kekuatan jurus
        self._element = element                                     # catat elemen jurus

    @property                                                       # (stiker) boleh DIBACA tanpa kurung
    def name(self):                                                 # cara membaca nama jurus
        return self._name                                           # berikan nama

    @property                                                       # (stiker) boleh DIBACA
    def power(self):                                                # cara membaca kekuatan jurus
        return self._power                                          # berikan kekuatan

    def __str__(self):                                              # aturan tampilan kartu jurus saat di-print
        return f"{self._name} (Power {self._power}, {self._element})"  # contoh hasil: Flame Burst (Power 20, Fire)


class EvolveMixin:                                                  # ITEM TAMBAHAN (mixin): kemampuan evolusi
    """Kemampuan evolusi, ditempel lewat multiple inheritance."""   # catatan: ditempel lewat multiple inheritance

    def evolve(self):                                               # jurus EVOLUSI
        if self.level < 16:                                         # kalau level monster kurang dari 16...
            print(f"{self.name} belum bisa evolusi (butuh Lv 16)")  # ...layar: belum bisa evolusi (BARIS 29 di tabel 4c)
            return False                                            # ...berhenti, hasilnya gagal
        self._attack += 10                                          # kalau lolos: attack naik 10
        self._max_hp += 20                                          # HP maksimal naik 20
        self._hp = self._max_hp                                     # HP langsung penuh
        print(f"{self.name} berevolusi! ATK={self._attack}, HP={self._max_hp}")  # layar: stat baru setelah evolusi
        return True                                                 # hasilnya berhasil


class Evomon:                                                       # CETAKAN MONSTER (orang tua semua monster)
    total_evomon = 0                      # class attribute  | HITUNGAN jumlah monster yang sudah lahir (milik bersama)
    VALID_ELEMENTS = ("Fire", "Water", "Grass")                     # daftar elemen yang diizinkan

    def __init__(self, name, element, level, max_hp, attack, move_data):  # proses LAHIR monster
        if not Evomon.is_valid_element(element):                    # kalau elemennya tidak ada di daftar...
            raise ValueError(f"Elemen tidak valid: {element}")      # ...BUNYIKAN ALARM dan batalkan kelahiran
        self._name = name                                           # isi kartu status: nama
        self._element = element                                     # elemen
        self._max_hp = max_hp                                       # HP maksimal
        self._hp = max_hp                                           # HP sekarang = penuh
        self._attack = attack                                       # attack
        self.level = level                # lewat setter  | level masuk lewat PENJAGA GERBANG (baris 70-74)
        self._moves = [Move(n, p, element) for (n, p) in move_data]  # lahirkan jurus-jurusnya (COMPOSITION: lahir bersama monster)
        Evomon.total_evomon += 1                                    # hitungan monster bertambah 1

    @property                                                       # (stiker) boleh DIBACA
    def name(self):                                                 # cara membaca nama
        return self._name                                           # berikan nama

    @property                                                       # (stiker) boleh DIBACA
    def element(self):                                              # cara membaca elemen
        return self._element                                        # berikan elemen

    @property                                                       # (stiker) boleh DIBACA
    def hp(self):                                                   # cara membaca HP
        return self._hp                                             # berikan HP sekarang

    @property                                                       # (stiker) boleh DIBACA
    def level(self):                                                # cara membaca level
        return self._level                                          # berikan level

    @level.setter                                                   # PENJAGA GERBANG level: aktif tiap kali level diisi
    def level(self, value):                                         # value = angka yang mau dimasukkan
        if not isinstance(value, int) or value < 1 or value > 100:  # bukan angka bulat? atau di bawah 1? atau di atas 100?
            raise ValueError("Level harus 1-100")                   # ALARM penolakan (BARIS 73 di tabel 4c)
        self._level = value                                         # lolos: level disimpan

    @property                                                       # (stiker) boleh DIBACA
    def is_fainted(self):                                           # apakah PINGSAN?
        return self._hp == 0                                        # pingsan kalau HP tepat 0

    @staticmethod                                                   # (stiker) alat pengecek, tidak butuh karakter tertentu
    def is_valid_element(e):                                        # cek elemen
        return e in Evomon.VALID_ELEMENTS                           # benar jika elemen ada di daftar

    @classmethod                                                    # (stiker) jalur lahir khusus
    def starter(cls, name):                                         # PAKET PEMULA; cls = cetakan yang memanggil (FireEvomon dst.)
        if cls is Evomon:                                           # kalau yang meminta Evomon umum...
            raise TypeError("Pakai subclass: FireEvomon/WaterEvomon/GrassEvomon")  # ...tolak: harus pilih Fire/Water/Grass
        return cls(name, 5, 45, 12, cls.DEFAULT_MOVES)              # lahirkan: Lv 5, HP 45, attack 12, jurus bawaan

    def type_multiplier(self, target):                              # aturan elemen bawaan
        return 1.0                                                  # tidak unggul/lemah (x1,0); anak-anaknya menimpa

    def attack_target(self, target, move_index=0):                  # jurus MENYERANG (move_index 0 = jurus pertama)
        move = self._moves[move_index]                              # ambil jurus yang dipilih
        damage = int((move.power + self._attack) * self.type_multiplier(target))  # HITUNG damage = (kekuatan jurus + attack) x pengali elemen
        target.take_damage(damage)                                  # lawan menerima damage
        print(f"{self.name} memakai {move.name} -> {target.name} -{damage} HP (sisa {target.hp})")  # LOG SERANGAN (BARIS 97 di tabel 4c)
        return damage                                               # hasilnya: besar damage

    def take_damage(self, amount):                                  # jurus TERLUKA
        self._hp = max(0, self._hp - amount)                        # HP berkurang, tapi tidak pernah di bawah 0

    def __eq__(self, other):                                        # aturan arti '==' untuk monster (BARIS 103)
        return (isinstance(other, Evomon) and                       # lawan bandingnya harus monster juga, dan...
                (self._name, self._element, self._level) ==         # ...nama, elemen, level milikku...
                (other._name, other._element, other._level))        # ...sama dengan milik lawan bandingnya?

    def __hash__(self):                                             # pelengkap __eq__ (tidak perlu dihafal)
        return hash((self._name, self._element, self._level))       # pelengkap __eq__

    def __str__(self):                                              # aturan tampilan kartu monster
        return f"{self._name} [{self._element}] Lv{self._level} HP {self._hp}/{self._max_hp}"  # contoh: Flamy [Fire] Lv5 HP 45/45


class FireEvomon(Evomon, EvolveMixin):                              # MONSTER API = anak Evomon + item evolusi
    DEFAULT_MOVES = [("Flame Burst", 20), ("Tackle", 10)]           # jurus bawaan monster api

    def __init__(self, name, level, max_hp, attack, move_data):     # proses lahir monster api
        super().__init__(name, "Fire", level, max_hp, attack, move_data)  # teruskan ke orang tua (Evomon), sebut elemen 'Fire'

    def type_multiplier(self, target):                              # aturan elemen API (menimpa versi umum)
        if target.element == "Grass":                               # lawan rumput...
            return 1.5                                              # ...api unggul (x1,5)
        if target.element == "Water":                               # lawan air...
            return 0.5                                              # ...api lemah (x0,5)
        return 1.0                                                  # selain itu netral


class WaterEvomon(Evomon, EvolveMixin):                             # MONSTER AIR = anak Evomon + item evolusi
    DEFAULT_MOVES = [("Aqua Jet", 20), ("Tackle", 10)]              # jurus bawaan monster air

    def __init__(self, name, level, max_hp, attack, move_data):     # proses lahir monster air
        super().__init__(name, "Water", level, max_hp, attack, move_data)  # teruskan ke orang tua, sebut elemen 'Water'

    def type_multiplier(self, target):                              # aturan elemen AIR (menimpa versi umum)
        if target.element == "Fire":                                # lawan api...
            return 1.5                                              # ...air unggul (x1,5)
        if target.element == "Grass":                               # lawan rumput...
            return 0.5                                              # ...air lemah (x0,5)
        return 1.0                                                  # selain itu netral


class GrassEvomon(Evomon, EvolveMixin):                             # MONSTER RUMPUT = anak Evomon + item evolusi
    DEFAULT_MOVES = [("Leaf Storm", 20), ("Tackle", 10)]            # jurus bawaan monster rumput

    def __init__(self, name, level, max_hp, attack, move_data):     # proses lahir monster rumput
        super().__init__(name, "Grass", level, max_hp, attack, move_data)  # teruskan ke orang tua, sebut elemen 'Grass'

    def type_multiplier(self, target):                              # aturan elemen RUMPUT (menimpa versi umum)
        if target.element == "Water":                               # lawan air...
            return 1.5                                              # ...rumput unggul (x1,5)
        if target.element == "Fire":                                # lawan api...
            return 0.5                                              # ...rumput lemah (x0,5)
        return 1.0                                                  # selain itu netral


class BattleSide(ABC):                                              # KERANGKA UMUM pihak bertarung (abstract: tidak bisa dibuat langsung)
    """Pihak yang bertarung (Trainer atau Evomon liar)."""          # catatan: bisa pelatih atau monster liar

    def __init__(self, name):                                       # proses lahir: butuh nama
        self._name = name                                           # catat nama pihak

    @property                                                       # (stiker) boleh DIBACA
    def name(self):                                                 # cara membaca nama
        return self._name                                           # berikan nama

    @abstractmethod                                                 # (stiker) WAJIB ditulis ulang oleh anak-anaknya
    def first_alive(self):                                          # siapa monster yang masih hidup?
        pass                                                        # kosong di sini; isinya ditulis anak-anaknya


class Trainer(BattleSide):                                          # PELATIH = anak BattleSide
    MAX_TEAM = 5                                                    # tim maksimal 6 monster

    def __init__(self, name, coins):                                # proses lahir pelatih
        super().__init__(name)                                      # serahkan pencatatan nama ke BattleSide
        self.coins = coins                # lewat setter  | coins masuk lewat PENJAGA DOMPET (baris 184-188)
        self._team = []                                             # siapkan tim kosong

    @property                                                       # (stiker) boleh DIBACA
    def coins(self):                                                # cara membaca coins
        return self._coins                                          # berikan coins

    @coins.setter                                                   # PENJAGA DOMPET
    def coins(self, value):                                         # value = angka yang mau dimasukkan
        if not isinstance(value, int) or value < 0:                 # bukan angka bulat? atau minus?
            raise ValueError("Coins tidak boleh negatif")           # ALARM penolakan coins (BARIS 187 di tabel 4c)
        self._coins = value                                         # lolos: coins disimpan

    def add_evomon(self, e):              # AGGREGATION  | jurus pelatih: TAMBAH monster ke tim
        if len(self._team) >= Trainer.MAX_TEAM:                     # kalau tim sudah penuh (6)...
            raise ValueError("Tim penuh")                           # ...alarm: tim penuh
        self._team.append(e)                                        # masukkan monster ke tim (datang dari luar)

    def first_alive(self):                                          # cari monster pertama yang masih hidup
        for e in self._team:                                        # periksa tim satu per satu dari depan
            if not e.is_fainted:                                    # kalau belum pingsan...
                return e                                            # ...dialah yang maju
        return None                                                 # semua pingsan: hasil kosong

    def __str__(self):                                              # tampilan kartu pelatih
        return f"Trainer {self._name} ({len(self._team)} Evomon, {self._coins} coins)"  # contoh: Trainer Ash (2 Evomon, 100 coins)


class WildEncounter(BattleSide):                                    # MONSTER LIAR (tanpa pelatih) = anak BattleSide
    def __init__(self, evomon):           # AGGREGATION: evomon dibuat di luar  | lahir: butuh satu monster
        super().__init__("Evomon Liar")                             # nama pihaknya: Evomon Liar
        self._evomon = evomon                                       # simpan monster dari luar

    def first_alive(self):                                          # siapa yang masih hidup?
        if not self._evomon.is_fainted:                             # kalau belum pingsan...
            return self._evomon                                     # ...dialah yang maju
        return None                                                 # sudah pingsan: hasil kosong


class Battle:                                                       # ARENA pertarungan
    def __init__(self, side_a, side_b):   # ASSOCIATION  | lahir: butuh dua pihak
        self._side_a = side_a                                       # simpan pihak A
        self._side_b = side_b                                       # simpan pihak B

    def run(self):                                                  # jurus arena: JALANKAN pertarungan
        turn = 1                                                    # mulai dari turn 1
        while self._side_a.first_alive() is not None and self._side_b.first_alive() is not None:  # SELAMA kedua pihak masih punya monster hidup, ulangi
            print(f"--- Turn {turn} ---")                           # tulis nomor turn (BARIS 224 di tabel 4c)
            a = self._side_a.first_alive()                          # pihak A kirim monster terdepan yang hidup
            b = self._side_b.first_alive()                          # pihak B kirim monster terdepan yang hidup
            a.attack_target(b, 0)                                   # A menyerang B (jurus pertama)
            if not b.is_fainted:                                    # kalau B belum pingsan...
                b.attack_target(a, 0)                               # ...B membalas
            turn += 1                                               # lanjut ke turn berikutnya
        winner = self._side_a if self._side_a.first_alive() is not None else self._side_b  # tentukan pemenang: A jika masih punya monster hidup, kalau tidak B
        print(f"Pemenang: {winner.name}")                           # umumkan pemenang (BARIS 232 di tabel 4c)
        return winner                                               # hasil: pemenang


if __name__ == "__main__":                                          # TOMBOL PLAY: baris di bawah ini jalan hanya jika file dijalankan langsung
    ash = Trainer("Ash", 100)                                       # lahirkan pelatih Ash (100 coins)
    gary = Trainer("Gary", 100)                                     # lahirkan pelatih Gary (100 coins)
    flamy = FireEvomon.starter("Flamy")                             # lahirkan monster api Flamy (paket pemula)
    leafy = GrassEvomon.starter("Leafy")                            # lahirkan monster rumput Leafy
    aquaro = WaterEvomon.starter("Aquaro")                          # lahirkan monster air Aquaro
    ash.add_evomon(flamy)                                           # Ash memasukkan Flamy ke tim
    ash.add_evomon(leafy)                                           # Ash memasukkan Leafy ke tim
    gary.add_evomon(aquaro)                                         # Gary memasukkan Aquaro ke tim

    print(ash)                                                      # layar: kartu Ash
    print(gary)                                                     # layar: kartu Gary
    print(flamy)                                                    # layar: kartu Flamy
    print(f"Total Evomon: {Evomon.total_evomon}")                   # layar: jumlah monster yang sudah lahir (3)

    # percobaan nilai tidak valid (validasi setter)
    try:                                                            # COBA...
        flamy.level = 150                                           # ...beri Flamy level 150 (akan DITOLAK, alarm di baris 73)
    except ValueError as err:                                       # kalau alarm berbunyi, tangkap pesannya di 'err'
        print(f"Error: {err}")                                      # layar: pesan penolakan
    try:                                                            # COBA...
        ash.coins = -50                                             # ...isi coins Ash -50 (akan DITOLAK, alarm di baris 187)
    except ValueError as err:                                       # kalau alarm berbunyi, tangkap pesannya
        print(f"Error: {err}")                                      # layar: pesan penolakan

    # perbandingan dua object dengan ==
    clone = FireEvomon.starter("Flamy")                             # lahirkan KEMBARAN Flamy
    print(f"flamy == clone  : {flamy == clone}")                    # tanya: Flamy sama dengan kembarannya? -> True
    print(f"flamy == aquaro : {flamy == aquaro}")                   # tanya: Flamy sama dengan Aquaro? -> False
    print("MRO: [" + ", ".join(c.__name__ for c in FireEvomon.__mro__) + "]")  # layar: urutan mencari kemampuan Flamy (MRO)

    # skenario: Trainer vs Trainer
    Battle(ash, gary).run()                                         # ARENA: Ash vs Gary, jalankan pertarungan
    print(flamy)                                                    # layar: kartu Flamy sesudah bertarung (HP 0)
    flamy.evolve()                                                  # coba evolusi (gagal: Lv 5 kurang dari 16)
    del ash                                # AGGREGATION: Evomon tetap ada  | hapus Ash dari game
    print(f"Setelah Ash dihapus: {leafy}")                          # layar: Leafy masih ada

    # skenario: Trainer vs Evomon liar (polymorphism)
    brock = Trainer("Brock", 50)                                    # lahirkan pelatih Brock (50 coins)
    brock.add_evomon(GrassEvomon.starter("Bushy"))                  # lahirkan Bushy, langsung diberikan ke Brock
    wild = WildEncounter(WaterEvomon.starter("Wildy"))              # lahirkan Wildy, bungkus sebagai monster liar
    print("=== Battle melawan Evomon liar ===")                     # layar: pengumuman babak
    Battle(brock, wild).run()                                       # ARENA yang sama: Brock vs monster liar
