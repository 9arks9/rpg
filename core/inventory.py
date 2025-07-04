import json
import os

class Inventory:
    def __init__(self, eq_path="data/eq.json", active_eq_path="data/active_eq.json"):
        self.eq_path = eq_path
        self.active_eq_path = active_eq_path
        self.ekwipunek = []
        self.ekwipunek_na_sobie = []
        self.load_ekwipunek()
        self.load_ekwipunek_na_sobie()

    def save_ekwipunek(self):
        with open(self.eq_path, "w", encoding="utf-8") as f:
            json.dump(self.ekwipunek, f, indent=4, ensure_ascii=False)
    def save_ekwipunek_na_sobie(self):
        with open(self.active_eq_path, "w", encoding="utf-8") as f:
            json.dump(self.ekwipunek_na_sobie, f, indent=4, ensure_ascii=False)
    def load_ekwipunek(self):
        if os.path.exists(self.eq_path):
            with open(self.eq_path, encoding="utf-8") as f:
                self.ekwipunek = json.load(f)
    def load_ekwipunek_na_sobie(self):
        if os.path.exists(self.active_eq_path):
            with open(self.active_eq_path, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    self.ekwipunek_na_sobie = data
                else:
                    self.ekwipunek_na_sobie = []
        else:
            self.ekwipunek_na_sobie = []

    def dodaj_do_ekwipunek(self, loot):
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
        if isinstance(nowy, dict) and nowy.get("max_ilosc"):
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
