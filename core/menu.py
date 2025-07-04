import os
from player import Gracz
from enemy import Przeciwnik
from combat import walcz
from save_system import save_game, load_game
from inventory import Inventory

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def show_main_menu():
    gracz = None

    while True:
        clear_screen()
        print("\n=== MENU GŁÓWNE ===")
        print("1. Nowa gra")
        print("2. Wczytaj grę")
        print("3. Wyjście")

        choice = input("Wybierz opcję (1-3): ")

        if choice == "1":
            gracz = start_new_game()
            game_loop(gracz)
        elif choice == "2":
            gracz = load_existing_game()
            if gracz:
                game_loop(gracz)
        elif choice == "3":
            print("👋 Do zobaczenia!")
            break
        else:
            print("❌ Nieprawidłowy wybór. Spróbuj ponownie.")

def start_new_game():
    nazwa = input("Podaj imię gracza: ")
    gracz = Gracz(nazwa=nazwa)
    print("🎮 Nowa gra rozpoczęta.")
    print(gracz)
    save_game(gracz)
    return gracz

def load_existing_game():
    gracz = load_game()
    if gracz:
        print("📂 Wczytano dane gracza:")
        print(gracz)
    return gracz

def flatten_ekwipunek(ekwipunek):
    # Spłaszcza listę, jeśli są zagnieżdżone listy
    if not ekwipunek:
        return []
    result = []
    for item in ekwipunek:
        if isinstance(item, list):
            result.extend(flatten_ekwipunek(item))
        else:
            result.append(item)
    return result

def pretty_print_ekwipunek(ekwipunek, tytul="Ekwipunek"):
    ekwipunek = flatten_ekwipunek(ekwipunek)
    print(f"\n--- {tytul} ---")
    if not ekwipunek:
        print("(pusto)")
        return
    for item in ekwipunek:
        if not isinstance(item, dict):
            print(f"- {item}")
            continue
        ilosc = item.get('ilosc', 1)
        ilosc_str = f" x{ilosc}" if ilosc > 1 else ""
        print(f"- {item.get('nazwa', 'Nieznany przedmiot')}{ilosc_str} (ID: {item.get('id')})")
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

def get_bonus_stats(gracz):
    atak_bonus = 0
    for item in gracz.pokaz_ekwipunek_na_sobie():
        if isinstance(item, dict) and item.get("ubieralne") and item.get("wymagania", 0) <= gracz.level:
            atak_bonus += item.get("atak", 0)
    return atak_bonus

def wait_for_user():
    input("\nNaciśnij Enter, aby kontynuować...")

def inventory_menu(gracz):
    while True:
        clear_screen()
        print("\n=== EKWIPUNEK ===")
        print("Ekwipunek na sobie:")
        pretty_print_ekwipunek(gracz.pokaz_ekwipunek_na_sobie(), tytul="Ekwipunek na sobie")
        print("\nTwój ekwipunek:")
        pretty_print_ekwipunek(gracz.pokaz_ekwipunek())
        print("\n1. Załóż przedmiot")
        print("2. Zdejmij przedmiot")
        print("3. Użyj mikstury")
        print("4. Powrót do gry")
        print("5. Wyrzuć przedmiot z ekwipunku")
        print(f"\n{gracz.nazwa} [{int(gracz.hp)}/{int(gracz.max_hp)}]")
        print(f"Poziom [{gracz.level}]-[{gracz.xp}/{gracz.max_xp}]")
        choice = input("Wybierz opcję (1-5): ")
        if choice == "1":
            try:
                item_id = int(input("Podaj ID przedmiotu do założenia: "))
            except ValueError:
                print("Nieprawidłowy ID!")
                wait_for_user()
                continue
            for item in gracz.pokaz_ekwipunek():
                if isinstance(item, dict) and item.get("id") == item_id:
                    if not item.get("ubieralne"):
                        print("Tego przedmiotu nie można założyć!")
                        wait_for_user()
                        break
                    if item.get("wymagania", 0) > gracz.level:
                        print("Za niski poziom na ten przedmiot!")
                        wait_for_user()
                        break
                    if item.get("atak", 0) > 0:
                        from weapons import zaloz
                        zaloz(gracz, item_id)
                        break
                    else:
                        from armors import zaloz
                        zaloz(gracz, item_id)
                        break
            else:
                print("Nie masz takiego przedmiotu w ekwipunku!")
                wait_for_user()
        elif choice == "2":
            try:
                item_id = int(input("Podaj ID przedmiotu do zdjęcia: "))
            except ValueError:
                print("Nieprawidłowy ID!")
                wait_for_user()
                continue
            for item in gracz.pokaz_ekwipunek_na_sobie():
                if isinstance(item, dict) and item.get("id") == item_id:
                    gracz.zdejmij_ekwipunek(item)
                    print(f"Zdjęto przedmiot: {item.get('nazwa')}")
                    # Po zdjęciu odśwież status
                    atak_bonus = get_bonus_stats(gracz)
                    print(f"\n{gracz.nazwa} [{int(gracz.hp)}/{int(gracz.max_hp)}]")
                    print(f"Poziom [{gracz.level}]-[{gracz.xp}/{gracz.max_xp}]")
                    print(f"Atak: {gracz.atak} (+{atak_bonus}) = {gracz.atak + atak_bonus}")
                    print(f"Zdrowie: {gracz.zdrowie}")
                    print(f"Obrona: {gracz.obrona}")
                    wait_for_user()
                    break
            else:
                print("Nie masz takiego przedmiotu na sobie!")
                wait_for_user()
        elif choice == "3":
            try:
                item_id = int(input("Podaj ID mikstury do użycia: "))
            except ValueError:
                print("Nieprawidłowy ID!")
                wait_for_user()
                continue
            from potions import uzyj
            uzyj(gracz, item_id)
            wait_for_user()
        elif choice == "4":
            break
        elif choice == "5":
            try:
                item_id = int(input("Podaj ID przedmiotu do wyrzucenia z ekwipunku: "))
            except ValueError:
                print("Nieprawidłowy ID!")
                wait_for_user()
                continue
            for item in gracz.pokaz_ekwipunek():
                if isinstance(item, dict) and item.get("id") == item_id:
                    gracz.inventory.usun_z_ekwipunek(item)
                    print(f"Wyrzucono przedmiot: {item.get('nazwa')}")
                    wait_for_user()
                    break
            else:
                print("Nie masz takiego przedmiotu w ekwipunku!")
                wait_for_user()
        else:
            print("❌ Nieprawidłowy wybór.")
            wait_for_user()

def game_loop(gracz):
    def pokaz_status():
        atak_bonus = get_bonus_stats(gracz)
        print(gracz)
        if atak_bonus:
            print(f"[Bonus] Atak z ekwipunku na sobie: +{atak_bonus}")
            print(f"[SUMA] Atak całkowity: {gracz.atak + atak_bonus}")

    while True:
        clear_screen()
        print("\n=== MENU GRY ===")
        print("1. Pokaż status")
        print("2. Walcz z potworem")
        print("3. Zapisz grę")
        print("4. Ekwipunek")
        print("5. Wyjście do menu głównego")

        choice = input("Wybierz opcję (1-5): ")

        if choice == "1":
            pokaz_status()
            wait_for_user()
        elif choice == "2":
            clear_screen()
            potwor = Przeciwnik.utworz("wilk")
            if potwor:
                wynik, loot = walcz(gracz, potwor)
                if wynik == "wygrana":
                    print("🎉 Gratulacje! Wygrałeś walkę.")
                elif wynik == "przegrana":
                    print("💀 Niestety, przegrałeś. Gra się kończy.")
                    break
        elif choice == "3":
            save_game(gracz)
        elif choice == "4":
            inventory_menu(gracz)
        elif choice == "5":
            print("🔙 Powrót do menu głównego.")
            break
        else:
            print("❌ Nieprawidłowy wybór.")
