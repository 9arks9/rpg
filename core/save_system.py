import json
import os
from player import Gracz
from inventory import Inventory

SAVE_DIR = "data"
SAVE_FILE = os.path.join(SAVE_DIR, "savegame.json")
EQ_FILE = os.path.join(SAVE_DIR, "eq.json")
ACTIVE_EQ_FILE = os.path.join(SAVE_DIR, "active_eq.json")

def ensure_save_dir():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def save_game(gracz: Gracz):
    ensure_save_dir()
    try:
        with open(SAVE_FILE, "w", encoding="utf-8") as f:
            json.dump(gracz.to_dict(), f, indent=4, ensure_ascii=False)
        gracz.inventory.save_ekwipunek()
        gracz.inventory.save_ekwipunek_na_sobie()
        print("✅ Gra została zapisana.")
    except Exception as e:
        print(f"❌ Błąd zapisu gry: {e}")

def load_game():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        gracz = Gracz.from_dict(data)
        gracz.inventory.load_ekwipunek()
        gracz.inventory.load_ekwipunek_na_sobie()
        print("✅ Gra została wczytana.")
        return gracz
    except FileNotFoundError:
        print("⚠️ Nie znaleziono zapisu gry.")
        return None
    except Exception as e:
        print(f"❌ Błąd wczytywania gry: {e}")
        return None
