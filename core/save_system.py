import json
import os
from player import Gracz

SAVE_DIR = "data"
SAVE_FILE = os.path.join(SAVE_DIR, "savegame.json")

def ensure_save_dir():
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

def save_game(gracz: Gracz):
    ensure_save_dir()
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(gracz.to_dict(), f, indent=4)
        print("✅ Gra została zapisana.")
    except Exception as e:
        print(f"❌ Błąd zapisu gry: {e}")

def load_game():
    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
        gracz = Gracz.from_dict(data)
        print("✅ Gra została wczytana.")
        return gracz
    except FileNotFoundError:
        print("⚠️ Nie znaleziono zapisu gry.")
        return None
    except Exception as e:
        print(f"❌ Błąd wczytywania gry: {e}")
        return None
