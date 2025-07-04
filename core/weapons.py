import json
from inventory import Inventory

with open("data/items/weapons.json", encoding="utf-8") as f:
    WEAPONS = json.load(f)

def zaloz(gracz, weapon_id):
    inv = gracz.inventory
    # Znajdź broń do założenia
    item_to_wear = None
    for item in inv.ekwipunek:
        if isinstance(item, dict) and item.get("id") == weapon_id:
            item_to_wear = item
            break
    if not item_to_wear:
        print("Nie masz tej broni w ekwipunku!")
        return False
    # Dodaj slot jeśli nie ma
    if "slot" not in item_to_wear:
        item_to_wear["slot"] = "broń"
    # Sprawdź czy już jest broń na sobie i podmień
    for item in inv.ekwipunek_na_sobie[:]:
        if item.get("slot", "broń") == "broń":
            inv.ekwipunek_na_sobie.remove(item)
            inv.ekwipunek.append(item)
            print(f"Zdjęto broń: {item.get('nazwa')}")
    inv.ekwipunek.remove(item_to_wear)
    inv.ekwipunek_na_sobie.append(item_to_wear)
    inv.save_ekwipunek()
    inv.save_ekwipunek_na_sobie()
    print(f"Założono broń: {item_to_wear['nazwa']}")
    return True
