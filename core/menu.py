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

def game_loop(gracz):
    while True:
        print("\n=== MENU GRY ===")
        print("1. Pokaż status")
        print("2. Walcz z potworem")
        print("3. Zapisz grę")
        print("4. Wyjście do menu głównego")

        choice = input("Wybierz opcję (1-4): ")

        if choice == "1":
            print(gracz)
        elif choice == "2":
            potwor = Przeciwnik.utworz("krolik")
            if potwor:
                wynik, loot = walcz(gracz, potwor)
                if wynik == "wygrana":
                    print("🎉 Gratulacje! Wygrałeś walkę.")
                    # Możesz dodać system przedmiotów na podstawie loot
                elif wynik == "przegrana":
                    print("💀 Niestety, przegrałeś. Gra się kończy.")
                    break
        elif choice == "3":
            save_game(gracz)
        elif choice == "4":
            print("🔙 Powrót do menu głównego.")
            break
        else:
            print("❌ Nieprawidłowy wybór.")
