import json
import os
from player import Gracz

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
        with open(EQ_FILE, "w", encoding="utf-8") as f:
            json.dump(gracz.ekwipunek, f, indent=4, ensure_ascii=False)
        with open(ACTIVE_EQ_FILE, "w", encoding="utf-8") as f:
            json.dump(gracz.ekwipunek_na_sobie, f, indent=4, ensure_ascii=False)
        print("✅ Gra została zapisana.")
    except Exception as e:
        print(f"❌ Błąd zapisu gry: {e}")

def load_game():
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        gracz = Gracz.from_dict(data)
        if os.path.exists(EQ_FILE):
            with open(EQ_FILE, encoding="utf-8") as f:
                gracz.ekwipunek = json.load(f)
        if os.path.exists(ACTIVE_EQ_FILE):
            with open(ACTIVE_EQ_FILE, encoding="utf-8") as f:
                gracz.ekwipunek_na_sobie = json.load(f)
        print("✅ Gra została wczytana.")
        return gracz
    except FileNotFoundError:
        print("⚠️ Nie znaleziono zapisu gry.")
        return None
    except Exception as e:
        print(f"❌ Błąd wczytywania gry: {e}")
        return None
