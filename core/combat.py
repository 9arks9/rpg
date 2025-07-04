from player import Gracz
from enemy import Przeciwnik
import random
import json
import os
import time

def pretty_print_loot(loot):
    if not loot:
        print("Brak lootu.")
        return
    print("\n--- Zdobycze ---")
    for item in loot:
        print(f"- {item.get('nazwa', 'Nieznany przedmiot')} (ID: {item.get('id')})")
        if 'opis' in item:
            print(f"  Opis: {item['opis']}")
        if 'atak' in item:
            print(f"  Atak: {item['atak']}")
        if 'trwalosc' in item:
            print(f"  Trwałość: {item['trwalosc']}")
        if 'wymagania' in item:
            print(f"  Wymagania: {item['wymagania']}")
        if 'cena' in item:
            print(f"  Cena: {item['cena']}")
        print()

def wait_for_user():
    input("\nNaciśnij Enter, aby kontynuować...")

def walcz(gracz: Gracz, przeciwnik: Przeciwnik):
    import copy
    import sys
    clear_screen = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    max_hp_enemy = getattr(przeciwnik, 'max_hp', None)
    if max_hp_enemy is None:
        max_hp_enemy = int(getattr(przeciwnik, 'hp', 0))
    while True:
        print(f"\n=== WALKA ===")
        print(f"{gracz.nazwa} [{int(gracz.hp)}/{int(gracz.max_hp)}]  VS  {przeciwnik.nazwa} [{int(przeciwnik.hp)}/{max_hp_enemy}]")
        print("----------------------------------------")
        while gracz.hp > 0 and przeciwnik.hp > 0:
            input("\n👉 Naciśnij Enter, aby zaatakować...")
            obrazenia, czy_kryt = gracz.zadaj_obrazenia_z_krytem()
            przeciwnik.hp = max(0, przeciwnik.hp - obrazenia)
            print(f"🗡️ {gracz.nazwa} zadaje {obrazenia} obrażeń!", end=" ")
            if czy_kryt:
                print("💥 CIOS KRYTYCZNY!")
            else:
                print()
            print(f"❤️ {przeciwnik.nazwa} ma teraz {int(przeciwnik.hp)} HP")
            time.sleep(1)
            if przeciwnik.hp <= 0:
                print(f"\n✅ {gracz.nazwa} pokonał {przeciwnik.nazwa}!")
                time.sleep(1)
                xp = przeciwnik.level * 5
                gracz.increase_xp(xp)
                loot = losuj_loot(przeciwnik.loot, przeciwnik)
                gracz.dodaj_do_ekwipunek(loot)
                pretty_print_loot(loot)
                print("🎉 Gratulacje! Wygrałeś walkę.")
                wynik = "wygrana"
                break
            obrazenia_wroga = przeciwnik.zadaj_obrazenia()
            gracz.przyjmij_obrazenia(obrazenia_wroga)
            print(f"💥 {przeciwnik.nazwa} zadaje {obrazenia_wroga} obrażeń!")
            print(f"❤️ {gracz.nazwa} ma teraz {int(gracz.hp)} HP")
            time.sleep(1)
            # --- Zmniejsz trwałość przedmiotów na sobie ---
            inv = gracz.inventory
            zmienione = False
            for item in inv.ekwipunek_na_sobie[:]:
                if isinstance(item, dict) and "trwalosc" in item:
                    item["trwalosc"] -= 1
                    if item["trwalosc"] <= 0:
                        print(f"❌ {item.get('nazwa', 'Przedmiot')} zużył się i został usunięty!")
                        inv.ekwipunek_na_sobie.remove(item)
                        zmienione = True
            if zmienione:
                inv.save_ekwipunek_na_sobie()
            # ---
            if gracz.hp <= 0:
                print(f"\n💀 {gracz.nazwa} został pokonany przez {przeciwnik.nazwa}...")
                print("💀 Niestety, przegrałeś. Gra się kończy.")
                time.sleep(1)
                loot = []
                wynik = "przegrana"
                break
        # Po walce
        inv = gracz.inventory
        inv.save_ekwipunek_na_sobie()  # Zapisz stan ekwipunku na sobie po walce
        print("\nNaciśnij Enter, aby kontynuować, lub SPACJĘ, aby walczyć z kolejnym takim samym przeciwnikiem: ")
        if os.name == 'nt':
            import msvcrt
            key = msvcrt.getch()
            if key in (b'\r', b'\n'):
                return wynik, loot
            elif key == b' ':
                nowy_przeciwnik = copy.deepcopy(przeciwnik)
                nowy_przeciwnik.hp = max_hp_enemy
                przeciwnik = nowy_przeciwnik
                continue
            else:
                continue
        else:
            key = input()
            if key == '':
                return wynik, loot
            elif key == ' ':
                nowy_przeciwnik = copy.deepcopy(przeciwnik)
                nowy_przeciwnik.hp = max_hp_enemy
                przeciwnik = nowy_przeciwnik
                continue
            else:
                continue

def losuj_loot(loot_lista, przeciwnik=None):
    if not loot_lista:
        return []
    # Załaduj wszystkie pliki z itemkami
    items = {}
    for fname in ["weapons.json", "potions.json", "armors.json"]:
        try:
            with open(f"data/items/{fname}", encoding="utf-8") as f:
                items.update(json.load(f))
        except Exception:
            pass
    # Szansa na drop czegokolwiek z potwora (domyślnie 1.0, można ustawiać w enemies.json)
    szansa_na_loot = 1.0
    if przeciwnik and hasattr(przeciwnik, 'szansa_na_loot'):
        szansa_na_loot = getattr(przeciwnik, 'szansa_na_loot', 1.0)
    elif isinstance(przeciwnik, dict):
        szansa_na_loot = przeciwnik.get('szansa_na_loot', 1.0)
    if random.random() > szansa_na_loot:
        return []  # Brak lootu z potwora
    wynik = []
    for item in items.values():
        if item.get("id") in loot_lista:
            # Szansa na drop danego przedmiotu (domyślnie 1.0, można ustawiać w pliku itema)
            szansa_na_drop = item.get("szansa_na_drop", 1.0)
            if random.random() <= szansa_na_drop:
                wynik.append(item)
    return wynik
