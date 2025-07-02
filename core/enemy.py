import json
import os

ENEMY_FILE = os.path.join("data", "enemies.json")

class Przeciwnik:
    _dane_potworow = {}

    def __init__(self, nazwa, level, hp, atak, loot):
        self.nazwa = nazwa
        self.level = level
        self.hp = hp
        self.atak = atak
        self.loot = loot  # lista indeksów przedmiotów

    def zadaj_obrazenia(self):
        return self.atak
    def przyjmij_obrazenia(self, wartosc):
        self.hp = max(0, self.hp - wartosc)
        return self.hp

    def __str__(self):
        return (f"👹 Przeciwnik: {self.nazwa}\n"
                f"📈 Poziom: {self.level}\n"
                f"❤️ HP: {self.hp}\n"
                f"🗡️ Atak: {self.atak}\n"
                f"🎁 Loot (indeksy): {self.loot}")

    @classmethod
    def _wczytaj_dane(cls):
        try:
            with open(ENEMY_FILE, "r") as f:
                cls._dane_potworow = json.load(f)
            print("📥 Wczytano dane przeciwników do pamięci.")
        except FileNotFoundError:
            print("❌ Plik enemies.json nie został znaleziony.")
        except Exception as e:
            print(f"❌ Błąd podczas wczytywania przeciwników: {e}")

    @classmethod
    def utworz(cls, nazwa_potwora):
        dane = cls._dane_potworow.get(nazwa_potwora)
        if dane:
            return cls(
                nazwa=dane["nazwa"],
                level=dane["level"],
                hp=dane["hp"],
                atak=dane["atak"],
                loot=dane["loot"]
            )
        else:
            print(f"❌ Nie znaleziono potwora o nazwie: {nazwa_potwora}")
            return None

# Automatyczne wczytanie danych przy załadowaniu modułu
Przeciwnik._wczytaj_dane()

# krolik = Przeciwnik.utworz("krolik")
# if krolik:
#     print(krolik)
# print(krolik.nazwa)
