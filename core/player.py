import random
import json
import os

class Gracz:
    def __init__(self, nazwa="Gracz", max_hp=100, hp=100, level=1, xp=0, max_xp=100, atak=5, obrona=1):
        self.nazwa = nazwa
        self.max_hp = max_hp
        self.hp = hp
        self.level = level
        self.xp = xp
        self.max_xp = max_xp
        self.punkty = 0
        self.atak = atak
        self.obrona = obrona
        self.zdrowie = 1
        self.szansa_kryt = 0.2
        self.mnoznik_kryt = 1.5
        self.ekwipunek = []  # Lista przedmiotów ekwipunku
        self.ekwipunek_na_sobie = []  # Lista przedmiotów na sobie

    def __str__(self):
        return f"\nStatus:\n{self.nazwa} [{int(self.hp)}/{int(self.max_hp)}]\nPoziom [{self.level}]-[{self.xp}/{self.max_xp}]\nAtrybuty:\n- {self.atak} atak\n- {self.zdrowie} zdrowie\n- {self.obrona} pancerz"

    def pokaz_nazwa(self):
        return self.nazwa
    def pokaz_level(self):
        return self.level
    def pokaz_hp(self):
        return self.hp
    def pokaz_max_hp(self):
        return self.max_hp
    def pokaz_xp(self):
        return self.xp
    def pokaz_max_xp(self):
        return self.max_xp
    def pokaz_punkty(self):
        return self.punkty
    def pokaz_atak(self):
        return self.atak
    def pokaz_obrona(self):
        return self.obrona
    def pokaz_zdrowie(self):
        return self.zdrowie
    def pokaz_szansa_kryt(self):
        return self.szansa_kryt

    def save_ekwipunek(self):
        with open("data/eq.json", "w", encoding="utf-8") as f:
            json.dump(self.ekwipunek, f, indent=4, ensure_ascii=False)
    def save_ekwipunek_na_sobie(self):
        with open("data/active_eq.json", "w", encoding="utf-8") as f:
            json.dump(self.ekwipunek_na_sobie, f, indent=4, ensure_ascii=False)
    def load_ekwipunek(self):
        if os.path.exists("data/eq.json"):
            with open("data/eq.json", encoding="utf-8") as f:
                self.ekwipunek = json.load(f)
    def load_ekwipunek_na_sobie(self):
        if os.path.exists("data/active_eq.json"):
            with open("data/active_eq.json", encoding="utf-8") as f:
                self.ekwipunek_na_sobie = json.load(f)

    def dodaj_do_ekwipunek(self, loot):
        # loot może być listą lub pojedynczym przedmiotem
        if not isinstance(loot, list):
            loot = [loot]
        for nowy in loot:
            if isinstance(nowy, list):
                for n in nowy:
                    self._dodaj_przedmiot_do_ekwipunku(n)
            else:
                self._dodaj_przedmiot_do_ekwipunku(nowy)
        self.save_ekwipunek()

    def _dodaj_przedmiot_do_ekwipunku(self, nowy):
        # Stackowanie tylko dla mikstur (id=0, max_ilosc=15)
        if isinstance(nowy, dict) and nowy.get("max_ilosc"):
            # Szukaj stacka z tym samym id i max_ilosc
            for item in self.ekwipunek:
                if isinstance(item, dict) and item.get("id") == nowy["id"] and item.get("max_ilosc"):
                    ilosc = item.get("ilosc", 1)
                    if ilosc < item["max_ilosc"]:
                        dodaj = min(nowy.get("ilosc", 1), item["max_ilosc"] - ilosc)
                        item["ilosc"] = ilosc + dodaj
                        nowy_ilosc = nowy.get("ilosc", 1) - dodaj
                        if nowy_ilosc > 0:
                            nowy = dict(nowy)
                            nowy["ilosc"] = nowy_ilosc
                            continue
                        return
            # Jeśli nie znaleziono stacka lub stack pełny, dodaj nowy slot
            nowy = dict(nowy)
            nowy["ilosc"] = nowy.get("ilosc", 1)
            self.ekwipunek.append(nowy)
        else:
            self.ekwipunek.append(nowy)

    def usun_z_ekwipunek(self, ekwipunek):
        if ekwipunek in self.ekwipunek:
            self.ekwipunek.remove(ekwipunek)
            self.save_ekwipunek()
        else:
            print("Przedmiot nie znajduje się w ekwipunku.")
    def zaloz_ekwipunek(self, ekwipunek):
        if ekwipunek in self.ekwipunek:
            self.ekwipunek.remove(ekwipunek)
            self.ekwipunek_na_sobie.append(ekwipunek)
            self.save_ekwipunek()
            self.save_ekwipunek_na_sobie()
        else:
            print("Nie masz tego przedmiotu w ekwipunku.")
    def zdejmij_ekwipunek(self, ekwipunek):
        if ekwipunek in self.ekwipunek_na_sobie:
            self.ekwipunek_na_sobie.remove(ekwipunek)
            self.ekwipunek.append(ekwipunek)
            self.save_ekwipunek()
            self.save_ekwipunek_na_sobie()
        else:
            print("Nie masz tego przedmiotu na sobie.")
    def pokaz_ekwipunek(self):
        self.load_ekwipunek()
        return self.ekwipunek
    def pokaz_ekwipunek_na_sobie(self):
        self.load_ekwipunek_na_sobie()
        return self.ekwipunek_na_sobie

    def ustaw_nazwa(self, wartosc):
        self.nazwa = wartosc
    def ustaw_level(self, wartosc):
        self.level = wartosc
    def ustaw_hp(self, wartosc):
        self.hp = wartosc
    def ustaw_max_hp(self, wartosc):
        self.max_hp = wartosc
    def ustaw_xp(self, wartosc):
        self.xp = wartosc
    def ustaw_max_xp(self, wartosc):
        self.max_xp = wartosc
    def ustaw_punkty(self, wartosc):
        self.punkty = wartosc
    def ustaw_atak(self, wartosc):
        self.atak = wartosc
    def ustaw_obrona(self, wartosc):
        self.obrona = wartosc
    def ustaw_zdrowie(self, wartosc):
        self.zdrowie = wartosc

    def decrease_hp(self, wartosc):
        return max(0, self.pokaz_hp() - wartosc)
    def decrease_punkty(self):
        self.punkty -= 1
    #ulecz hp
    def increase_hp(self, wartosc):
        if wartosc > 0:
            self.ustaw_hp(self.pokaz_hp() + wartosc)
    def increase_punkty(self):
        self.punkty += 5
    def increase_zdrowie(self, wartosc):
        self.zdrowie += wartosc

    def increase_level(self):
        self.level += 1
    def increase_atak(self, wartosc):
        self.atak += wartosc
    def increase_obrona(self, wartosc):
        self.obrona += wartosc

    def dodaj_punkt(self, atrybut, punktow):
        if atrybut == "hp":
            wartosc = 5
            self.increase_max_hp(wartosc * punktow)
            self.increase_hp(round(wartosc * 0.5, 0))
            print("Pomyslnie dodano punkt w HP\n")
            self.increase_zdrowie(punktow)
            self.punkty -= punktow
        elif atrybut == "atk":
            wartosc = 1
            self.increase_atak(wartosc * punktow)
            print("Pomyslnie dodano punkt w Atak\n")
            self.increase_atak(punktow)
            self.punkty -= punktow
        elif atrybut == "obr":
            wartosc = 1
            self.increase_obrona(wartosc * punktow)
            print("Pomyslnie dodano punkt w Obrona\n")
            self.increase_obrona(punktow)
            self.punkty -= punktow

    def ulepsz_atrybuty(self):
        print("Level up!")
        print("Ulepszanie atrybutow")
        print(f"Masz {self.punkty} punktow do rozdania")
        while self.punkty > 0:
            atrybut = input("Wybierz atrybut do ulepszenia (hp/atk/obr): ").lower()
            punktow = int(input("Ile punktow chcesz dodac? "))
            if punktow <= self.punkty:
                self.dodaj_punkt(atrybut, punktow)
            else:
                print("Nie masz wystarczajaco punktow!")
                print(f"Masz {self.punkty} punktow do rozdania")
                print(self)

    def increase_max_xp(self):
        #level up
        self.hp = self.max_hp
        self.ustaw_max_xp(self.pokaz_max_xp() + (self.pokaz_max_xp() * 0.5))
        self.increase_punkty()

    def increase_xp(self, wartosc):
        self.xp += wartosc
        print(f"\n**Zdobyto {wartosc} XP**")
        if self.xp >= self.max_xp:
            roznica = self.xp - self.max_xp
            self.increase_max_xp()
            self.ustaw_xp(0)
            self.xp += roznica
            self.increase_level()
            self.ulepsz_atrybuty()
        else:
            self.xp += wartosc

    def increase_max_hp(self, wartosc):
        self.ustaw_max_hp(self.pokaz_max_hp() + wartosc)

    def zadaj_obrazenia(self):
        return self.atak  # dodajemy losowy bonus do ataku
    def przyjmij_obrazenia(self, wartosc):
        self.hp -= max(0, wartosc - self.pokaz_obrona())

    def to_dict(self):
        return {
            "nazwa": self.nazwa,
            "max_hp": self.max_hp,
            "hp": self.hp,
            "level": self.level,
            "xp": self.xp,
            "max_xp": self.max_xp,
            "punkty": self.punkty,
            "atak": self.atak,
            "obrona": self.obrona,
            "zdrowie": self.zdrowie
        }

    @classmethod
    def from_dict(cls, data):
        gracz = cls(
            nazwa=data.get("nazwa", "Gracz"),
            max_hp=data.get("max_hp", 100),
            hp=data.get("hp", 100),
            level=data.get("level", 1),
            xp=data.get("xp", 0),
            max_xp=data.get("max_xp", 100),
            atak=data.get("atak", 1),
            obrona=data.get("obrona", 1)
        )
        gracz.punkty = data.get("punkty", 0)
        gracz.zdrowie = data.get("zdrowie", 1)
        return gracz

    def krytyczne_obrazenia_bonus(self, podstawowe_obrazenia):
        if random.random() < self.szansa_kryt:
            bonus = int(podstawowe_obrazenia * (self.mnoznik_kryt - 1))
            return bonus
        return 0

    def zadaj_obrazenia_z_krytem(self):
        bazowe = self.zadaj_obrazenia()
        bonus = self.krytyczne_obrazenia_bonus(bazowe)
        return bazowe + bonus, bonus > 0

#test
# ja = Gracz() 
# print(ja)
# ja.przyjmij_obrazenia(5)
# print(ja)
# ja.dodaj_punkt("hp")
# print(ja)
# ja.increase_xp(105)
# print(ja)
# print(ja.zadaj_obrazenia())

