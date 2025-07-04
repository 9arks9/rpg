from player import Gracz
from enemy import Przeciwnik
from combat import walcz
from save_system import save_game, load_game

def show_main_menu():
    gracz = None

    while True:
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

def game_loop(gracz):
    while True:
        print("\n=== MENU GRY ===")
        print("1. Pokaż status")
        print("2. Walcz z potworem")
        print("3. Zapisz grę")
        print("4. Sprawdź ekwipunek")
        print("5. Sprawdź ekwipunek na sobie")
        print("6. Wyjście do menu głównego")

        choice = input("Wybierz opcję (1-6): ")

        if choice == "1":
            print(gracz)
        elif choice == "2":
            potwor = Przeciwnik.utworz("krolik")
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
            pretty_print_ekwipunek(gracz.pokaz_ekwipunek())
        elif choice == "5":
            pretty_print_ekwipunek(gracz.pokaz_ekwipunek_na_sobie(), tytul="Ekwipunek na sobie")
        elif choice == "6":
            print("🔙 Powrót do menu głównego.")
            break
        else:
            print("❌ Nieprawidłowy wybór.")
