"""Program utama Game RPG Turn-Based Evomon (Tugas Pertemuan 9 - Exception Handling)."""

from exceptions import (
    EvomonError,
    ValidationError,
    InvalidLevelError,
    InvalidCoinsError,
    InvalidElementError,
    RuleViolationError,
    TeamFullError,
    FaintedEvomonError,
    EvolutionNotAllowedError,
    MoveNotFoundError,
)
from evomon import (
    Evomon,
    FireEvomon,
    WaterEvomon,
    GrassEvomon,
    Trainer,
    WildEncounter,
    Battle,
)


def coba_evolusi_dengan_log(evomon):
    """Contoh RE-RAISE: mencatat log di dalam fungsi, lalu melempar ulang ke pemanggil."""
    try:
        evomon.evolve()
    except EvolutionNotAllowedError:
        print(f"[LOG AUDIT] Percobaan evolusi gagal pada {evomon.name} (Lv{evomon.level})")
        raise


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

    # 1. Validasi Level (urutan except: spesifik InvalidLevelError -> umum ValidationError)
    try:
        flamy.level = 150
    except InvalidLevelError as err:
        print(f"Error Level: {err} (rentang sah: {err.min_level}-{err.max_level})")
    except ValidationError as err:
        print(f"Error Validasi: {err}")

    # 2. Validasi Coins (skenario berhasil & gagal dengan try/except/else/finally)
    for nilai_baru in (150, -50):
        try:
            ash.coins = nilai_baru
        except InvalidCoinsError as err:
            print(f"Error Coins: {err} (nilai ditolak: {err.value})")
        except ValidationError as err:
            print(f"Error Validasi: {err}")
        else:
            print(f"Coins Ash berhasil diubah menjadi {ash.coins}")
        finally:
            print(f"[finally] Validasi coins untuk nilai {nilai_baru} selesai")

    # 3. Validasi Elemen
    try:
        Evomon("Zappy", "Electric", 5, 45, 12, [("Thunder", 20)])
    except InvalidElementError as err:
        print(f"Error Elemen: {err}")
    except ValidationError as err:
        print(f"Error Validasi: {err}")

    # 4. Aturan Tim Penuh (maksimal 5 Evomon)
    penuh = Trainer("Penuh", 0)
    try:
        for i in range(1, 7):
            penuh.add_evomon(FireEvomon.starter(f"F{i}"))
    except TeamFullError as err:
        print(f"Error Tim: {err} (kapasitas {err.trainer_name}: {err.max_team})")
    except RuleViolationError as err:
        print(f"Error Aturan: {err}")

    # Perbandingan dua object dengan == dan MRO
    clone = FireEvomon.starter("Flamy")
    print(f"flamy == clone  : {flamy == clone}")
    print(f"flamy == aquaro : {flamy == aquaro}")
    print("MRO: [" + ", ".join(c.__name__ for c in FireEvomon.__mro__) + "]")

    # 5. Skenario Battle: Trainer vs Trainer
    try:
        battle_pvp = Battle(ash, gary)
        battle_pvp.run()
    except EvomonError as err:
        print(f"Battle gagal: {err}")
    else:
        for line in battle_pvp.log:
            print(line)
        print("Battle selesai tanpa error")
    finally:
        print("[finally] Sesi Battle Ash vs Gary ditutup")
    print(flamy)

    # 6. Aturan Evomon Pingsan (urutan spesifik -> umum)
    try:
        flamy.attack_target(leafy)
    except FaintedEvomonError as err:
        print(f"Error Serang: {err} (aksi ditolak: {err.role})")
    except RuleViolationError as err:
        print(f"Error Aturan: {err}")

    # 7. Aturan Evolusi (RE-RAISE + skenario gagal & berhasil)
    try:
        coba_evolusi_dengan_log(flamy)
    except EvolutionNotAllowedError as err:
        print(f"Error Evolusi: {err} -> butuh {err.missing_levels} level lagi")
    except RuleViolationError as err:
        print(f"Error Aturan: {err}")

    try:
        leafy.level = 16
        coba_evolusi_dengan_log(leafy)
    except EvolutionNotAllowedError as err:
        print(f"Error Evolusi: {err}")
    else:
        print(f"{leafy.name} berevolusi! ATK={leafy.attack}, HP={leafy.hp}/{leafy.max_hp}")
    finally:
        print(f"[finally] Pemeriksaan evolusi {leafy.name} selesai")

    # 8. EAFP + Exception Chaining (raise ... from IndexError)
    try:
        leafy.attack_target(aquaro, move_index=99)
    except FaintedEvomonError as err:
        print(f"Error Serang: {err}")
    except MoveNotFoundError as err:
        cause_name = type(err.__cause__).__name__ if err.__cause__ else "None"
        print(f"Error Jurus: {err} (penyebab asli: {cause_name})")
    except EvomonError as err:
        print(f"Error Aplikasi: {err}")

    # Uji EAFP khusus MoveNotFoundError pada target yang masih hidup
    wild_target = WaterEvomon.starter("Splashy")
    try:
        leafy.attack_target(wild_target, move_index=99)
    except MoveNotFoundError as err:
        cause_name = type(err.__cause__).__name__ if err.__cause__ else "None"
        print(f"Error Jurus (EAFP): {err} (penyebab asli: {cause_name})")
    except EvomonError as err:
        print(f"Error Aplikasi: {err}")

    # Bukti AGGREGATION
    del ash
    print(f"Setelah Ash dihapus: {leafy}")

    # Skenario: Trainer vs Evomon liar (polymorphism)
    brock = Trainer("Brock", 50)
    brock.add_evomon(GrassEvomon.starter("Bushy"))
    wild = WildEncounter(WaterEvomon.starter("Wildy"))
    print("=== Battle melawan Evomon liar ===")
    battle_wild = Battle(brock, wild)
    battle_wild.run()
    for line in battle_wild.log:
        print(line)
